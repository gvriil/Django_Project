from django.contrib import admin

from catalog.models import Category, Product, Contacts, BlogPost


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


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
