from django.core.cache import cache

from .models import Product


def get_cached_products():
    key = 'all_products'
    products = cache.get(key)
    if not products:
        products = list(Product.objects.all().filter(is_published=True))
        cache.set(key, products, timeout=60)  # Кеширует на 1 минуту
    return products
