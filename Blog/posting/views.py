"""
Views for Model Manis website
API-based views without database
"""
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from .utils.shopee_api import fetch_shopee_products, format_price
from .utils.instagram_api import fetch_instagram_feed, truncate_caption
import logging

logger = logging.getLogger(__name__)


def homepage(request):
    """
    Homepage view - display featured products from Shopee
    """
    try:
        # Fetch products from Shopee
        shopee_data = fetch_shopee_products(limit=12)
        products = shopee_data.get('products', [])
        
        # Get Instagram feed preview (first 6 posts)
        instagram_data = fetch_instagram_feed(limit=6)
        instagram_posts = instagram_data.get('media', [])
        
        context = {
            'products': products[:8],  # Show only 8 on homepage
            'instagram_posts': instagram_posts,
            'shopee_url': settings.SHOPEE_STORE_URL,
            'instagram_url': settings.INSTAGRAM_PROFILE_URL,
            'has_products': len(products) > 0,
            'has_instagram': len(instagram_posts) > 0,
        }
        
        return render(request, 'posting/homepage.html', context)
    
    except Exception as e:
        logger.error(f"Error in homepage view: {e}")
        # Return with empty data
        context = {
            'products': [],
            'instagram_posts': [],
            'shopee_url': settings.SHOPEE_STORE_URL,
            'instagram_url': settings.INSTAGRAM_PROFILE_URL,
            'has_products': False,
            'has_instagram': False,
            'error': 'Mohon maaf, terjadi kesalahan saat memuat data.'
        }
        return render(request, 'posting/homepage.html', context)


def product_list(request):
    """
    Product listing view - display all products from Shopee
    """
    try:
        # Get page number
        page_number = request.GET.get('page', 1)
        limit = 50
        
        try:
            page_number = int(page_number)
            offset = (page_number - 1) * limit
        except ValueError:
            page_number = 1
            offset = 0
        
        # Fetch products from Shopee
        shopee_data = fetch_shopee_products(limit=limit, offset=offset)
        products = shopee_data.get('products', [])
        total = shopee_data.get('total', 0)
        has_more = shopee_data.get('has_more', False)
        
        # Calculate pagination
        total_pages = (total + limit - 1) // limit if total > 0 else 1
        
        context = {
            'products': products,
            'page_number': page_number,
            'total_pages': total_pages,
            'has_previous': page_number > 1,
            'has_next': has_more and page_number < total_pages,
            'previous_page': page_number - 1,
            'next_page': page_number + 1,
            'total_products': total,
            'shopee_url': settings.SHOPEE_STORE_URL,
            'has_products': len(products) > 0,
        }
        
        return render(request, 'posting/product_list.html', context)
    
    except Exception as e:
        logger.error(f"Error in product_list view: {e}")
        context = {
            'products': [],
            'page_number': 1,
            'total_pages': 1,
            'has_previous': False,
            'has_next': False,
            'total_products': 0,
            'shopee_url': settings.SHOPEE_STORE_URL,
            'has_products': False,
            'error': 'Mohon maaf, terjadi kesalahan saat memuat produk.'
        }
        return render(request, 'posting/product_list.html', context)


def instagram_gallery(request):
    """
    Instagram gallery view - display Instagram feed
    """
    try:
        # Fetch Instagram feed
        instagram_data = fetch_instagram_feed(limit=24)
        media_items = instagram_data.get('media', [])
        profile_url = instagram_data.get('profile_url', settings.INSTAGRAM_PROFILE_URL)
        has_token = instagram_data.get('has_token', False)
        error_message = instagram_data.get('error', None)
        
        context = {
            'media_items': media_items,
            'profile_url': profile_url,
            'has_token': has_token,
            'has_media': len(media_items) > 0,
            'error': error_message,
            'instagram_username': 'modelmanis_rtl',
        }
        
        return render(request, 'posting/instagram.html', context)
    
    except Exception as e:
        logger.error(f"Error in instagram_gallery view: {e}")
        context = {
            'media_items': [],
            'profile_url': settings.INSTAGRAM_PROFILE_URL,
            'has_token': False,
            'has_media': False,
            'error': 'Mohon maaf, terjadi kesalahan saat memuat feed Instagram.',
            'instagram_username': 'modelmanis_rtl',
        }
        return render(request, 'posting/instagram.html', context)


def about_us(request):
    """
    About us page
    """
    context = {
        'shopee_url': settings.SHOPEE_STORE_URL,
        'instagram_url': settings.INSTAGRAM_PROFILE_URL,
    }
    return render(request, 'posting/about_us.html', context)


def contact(request):
    """
    Contact page
    """
    context = {
        'shopee_url': settings.SHOPEE_STORE_URL,
        'instagram_url': settings.INSTAGRAM_PROFILE_URL,
    }
    return render(request, 'posting/contact.html', context)
