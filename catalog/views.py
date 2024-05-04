# catalog/views.py
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from .forms import ProductForm, VersionInlineFormset, BlogPostForm
from .models import Product, Contacts, BlogPost, Versions
from .services import get_cached_products


def home(request):
    products = Product.objects.order_by('-created_at')

    paginator = Paginator(products, 4)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # This is the paginated products
        'title': 'Главная'
    }

    return render(request, 'catalog/home.html', context)


class ProductCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context_data['formset'] = VersionInlineFormset(self.request.POST)
        else:
            context_data['formset'] = VersionInlineFormset()
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        form.instance.slug = slugify(form.instance.name)
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект продукта
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context_data['formset'] = VersionInlineFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionInlineFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()  # Сохранение основных данных продукта

            if formset.is_valid():
                self.object.versions.update(is_current_version=False)  # сброс текущих версий
                versions = formset.save(commit=False)
                for version in versions:
                    version.product = self.object
                    version.save()
                formset.save_m2m()
        return super().form_valid(form)


def delete_version(request, version_id):
    version = get_object_or_404(Versions, id=version_id)
    product_id = version.product.id
    if request.method == 'POST':
        version.delete()
        messages.success(request, "Версия удалена успешно.")
        return redirect(reverse('catalog:product_detail', args=[product_id]))
    return redirect(reverse('catalog:product_detail', args=[product_id]))


class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Product
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        # Возвращаем только опубликованные продукты
        return get_cached_products()
        # return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for product in context['products']:
            product.current_version = product.versions.filter(is_current_version=True).first()

        return context


def set_current_version(request, version_id):
    version = get_object_or_404(Versions, id=version_id)
    with transaction.atomic():
        # Сначала сбрасываем флаг текущей версии у всех версий этого продукта
        Versions.objects.filter(product=version.product).update(is_current_version=False)

        # Затем устанавливаем выбранную версию как текущую
        version.is_current_version = True
        version.save()

    return redirect(reverse('catalog:product_detail', args=[version.product.id]))


def contact(request):
    contacts = Contacts.objects.get()
    context = {
        'contacts': contacts,
        'title': 'Контакты'

    }

    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name, phone, message)
    return render(request, 'catalog/contacts.html', context)


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     top_5 = Product.objects.order_by('-created_at').filter(~Q(id=pk))[:4]
#     return render(request, 'catalog/product_detail.html', {'product': product, 'top': top_5})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['top'] = Product.objects.order_by('-created_at').exclude(id=pk)[:4]
        return context

    def get_object(self):
        obj = super().get_object()
        print(f"Loaded product: {obj.name} with slug {obj.slug}")
        return obj


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'

    def get_queryset(self):
        """Возвращаем только опубликованные статьи."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs.get('pk')
    #     context['top'] = Product.objects.order_by('-created_at').exclude(id=pk)[:4]
    #     return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        if obj.views_count == 100:
            send_mail(
                'Поздравление с достижением!',
                'Статья "{}" достигла 100 просмотров.'.format(obj.title),
                settings.DEFAULT_FROM_EMAIL,
                ['your_email@yandex.ru'],
                fail_silently=False,
            )
        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'catalog/blogpost_form.html/'
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'created_at', 'is_published', 'views_count']
    template_name = 'catalog/blogpost_form.html/'
    success_url = reverse_lazy('catalog:blogpost_list')

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'slug': self.object.slug})



class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')
