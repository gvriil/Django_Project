# catalog/views.py
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Product, Contacts


def home(request):
    # Product.objects.all()[:5]
    new_products = Product.objects.order_by('-created_at')[:8]
    context = {'new_products': new_products}
    return render(request, 'catalog/home.html', context)


def contact(request):
    contacts = Contacts.objects.get()
    context = {'contacts': contacts}

    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name, phone, message)
    return render(request, 'catalog/contacts.html', context)
