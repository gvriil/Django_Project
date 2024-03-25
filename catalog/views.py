# catalog/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    template_name = 'catalog/blogpost_list.html/'


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'created_at', 'is_published', 'views_count']
    template_name = 'catalog/blogpost_form.html/'
    success_url = reverse_lazy('catalog:blogpost_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'slug', 'content', 'preview', 'created_at', 'is_published', 'views_count']
    template_name = 'catalog/blogpost_form.html/'
    success_url = reverse_lazy('catalog:blogpost_list')


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')
