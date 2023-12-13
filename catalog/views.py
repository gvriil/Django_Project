# catalog/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Contacts


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


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    top_5 = Product.objects.order_by('-created_at').filter(~Q(id=pk))[:4]
    return render(request, 'catalog/product_detail.html', {'product': product, 'top': top_5})

