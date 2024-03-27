from django.urls import path
from . import views
from .views import ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,\
    BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostDeleteView,\
    BlogPostUpdateView

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', views.BlogPostListView.as_view(), name='blogpost_list'),  # Список постов
    path('blog/add/', views.BlogPostCreateView.as_view(), name='blogpost_add'),  # Add post
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('blog/<int:pk>/delete', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]
