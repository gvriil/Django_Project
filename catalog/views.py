# catalog/views.py
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from .models import Product, Contacts, BlogPost


def home(request):
    # Product.objects.all()[:5]
    new_products = Product.objects.order_by('-created_at')
    paginator = Paginator(new_products, 4)
    pagenumber = request.GET.get("page")
    page = paginator.get_page(pagenumber)
    context = {
        'new_products': page,
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'picture', 'category', 'price', 'in_stock']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'picture', 'category', 'price', 'in_stock']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product
    paginate_by = 8


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['top'] = Product.objects.order_by('-created_at').exclude(id=pk)[:4]
        return context


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Возвращаем только опубликованные статьи."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['top'] = Product.objects.order_by('-created_at').exclude(id=pk)[:4]
        return context

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
    fields = ['title', 'content', 'preview', 'created_at', 'is_published', 'views_count']
    template_name = 'catalog/blogpost_form.html/'
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'slug', 'content', 'preview', 'created_at', 'is_published', 'views_count']
    template_name = 'catalog/blogpost_form.html/'

    def get_success_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.object.slug})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')
