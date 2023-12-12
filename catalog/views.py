# catalog/views.py
from django.shortcuts import render, get_object_or_404

from .models import Product, Contacts


def home(request):
    # Product.objects.all()[:5]
    new_products = Product.objects.order_by('-created_at')[:8]
    context = {
        'new_products': new_products,
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


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})
