from django.contrib import admin

from catalog.models import Category, Product, Contacts


# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'in_stock')
    list_filter = ('in_stock',)
    search_fields = ('name', 'description')


@admin.register(Contacts)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'town', 'email')

