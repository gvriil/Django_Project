from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    BlogPostDeleteView, \
    BlogPostUpdateView, ProductListView

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('product/', cache_page(60 * 15)(ProductListView.as_view()), name='product_list'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:version_id>/set_current_version/', views.set_current_version,
         name='set_current_version'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', views.BlogPostListView.as_view(), name='blogpost_list'),  # Список постов
    path('blog/add/', views.BlogPostCreateView.as_view(), name='blogpost_add'),  # Add post
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('blog/<slug:slug>/delete', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    path('version/delete/<int:version_id>/', views.delete_version, name='delete_version'),
]
