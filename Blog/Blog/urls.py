from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from posting import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (keep for admin access)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Homepage
    path('', views.homepage, name='homepage'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Categories
    path('categories/', views.category_list, name='category_list'),

    # About Us
    path('about/', views.about_us, name='about_us'),

    # Contact
    path('contact/', views.contact, name='contact'),

    # Management Views (for logged-in users)
    path('manage/', views.manage_dashboard, name='manage_dashboard'),
    path('manage/products/', views.manage_products, name='manage_products'),
    path('manage/products/add/', views.add_product, name='add_product'),
    path('manage/products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('manage/products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('manage/categories/', views.manage_categories, name='manage_categories'),
    path('manage/categories/add/', views.add_category, name='add_category'),
    path('manage/categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('manage/slider/', views.manage_slider, name='manage_slider'),
    path('manage/slider/add/', views.add_slide, name='add_slide'),
    path('manage/store-info/', views.manage_store_info, name='manage_store_info'),

    # API for search
    path('api/search/', views.search_products, name='search_products'),
    
    # Debug/Fix URLs (temporary)
    path('fix-slugs/', views.fix_category_slugs_view, name='fix_category_slugs'),

    # Include additional posting routes (for any remaining functionality)
    path('posting/', include('posting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
