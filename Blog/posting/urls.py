"""
URL configuration for posting app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('instagram/', views.instagram_gallery, name='instagram_gallery'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
]
