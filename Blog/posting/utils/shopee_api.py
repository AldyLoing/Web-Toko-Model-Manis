"""
Shopee API Utilities
Fetch product data from Shopee store
"""
import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def get_static_products():
    """
    Static product data as fallback when Shopee API is blocked
    Data should be updated manually from https://shopee.co.id/modelmanis34
    """
    return [
        {
            'itemid': 1,
            'shopid': 53252649,
            'name': 'Produk Fashion Wanita - Lihat Toko Kami',
            'price': 100000,
            'price_min': 50000,
            'price_max': 200000,
            'image': 'https://via.placeholder.com/300x300/FF6B35/FFFFFF?text=Model+Manis',
            'images': [],
            'stock': 999,
            'sold': 0,
            'historical_sold': 0,
            'liked_count': 0,
            'rating_star': 5.0,
            'url': settings.SHOPEE_STORE_URL,
        },
        {
            'itemid': 2,
            'shopid': 53252649,
            'name': 'Koleksi Pakaian Muslim - Kunjungi Shopee',
            'price': 150000,
            'price_min': 80000,
            'price_max': 250000,
            'image': 'https://via.placeholder.com/300x300/FF6B35/FFFFFF?text=Model+Manis',
            'images': [],
            'stock': 999,
            'sold': 0,
            'historical_sold': 0,
            'liked_count': 0,
            'rating_star': 5.0,
            'url': settings.SHOPEE_STORE_URL,
        },
        {
            'itemid': 3,
            'shopid': 53252649,
            'name': 'Aksesoris & Hijab - Lihat Koleksi Lengkap',
            'price': 75000,
            'price_min': 30000,
            'price_max': 150000,
            'image': 'https://via.placeholder.com/300x300/FF6B35/FFFFFF?text=Model+Manis',
            'images': [],
            'stock': 999,
            'sold': 0,
            'historical_sold': 0,
            'liked_count': 0,
            'rating_star': 5.0,
            'url': settings.SHOPEE_STORE_URL,
        },
    ]


def get_shop_id_from_username(username='modelmanis34'):
    """
    Get Shopee shop ID from username/slug
    """
    try:
        url = f'https://shopee.co.id/api/v4/shop/get_shop_detail'
        params = {'username': username}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': f'https://shopee.co.id/{username}',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('error') == 0 and data.get('data'):
            shop_id = data['data'].get('shopid')
            return shop_id
    except Exception as e:
        logger.error(f"Error getting shop ID: {e}")
    
    return None


def fetch_shopee_products(shop_id=None, limit=50, offset=0):
    """
    Fetch products from Shopee API via Cloudflare Worker Proxy
    
    Args:
        shop_id: Shopee shop ID (if None, try to get from env or resolve from username)
        limit: Number of products to fetch (max 50 per request)
        offset: Pagination offset
    
    Returns:
        dict: {
            'products': [...],
            'total': int,
            'has_more': bool
        }
    """
    # Get shop ID
    if not shop_id:
        shop_id = settings.SHOPEE_SHOP_ID
    
    if not shop_id:
        # Try to resolve from username
        shop_id = get_shop_id_from_username('modelmanis34')
        if not shop_id:
            logger.error("Cannot resolve Shopee shop ID")
            return get_fallback_result(limit)
    
    # Check cache
    cache_key = f'shopee_products_{shop_id}_{limit}_{offset}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        # Try Cloudflare Worker Proxy first (if configured)
        proxy_url = getattr(settings, 'SHOPEE_PROXY', None)
        
        if proxy_url:
            logger.info("Using Cloudflare Worker Proxy for Shopee API")
            url = proxy_url
            params = {
                'shopid': shop_id,
                'limit': limit,
                'offset': offset
            }
            headers = {
                'Accept': 'application/json',
            }
        else:
            # Fallback to direct API (will likely get 403)
            logger.warning("SHOPEE_PROXY not configured, using direct API (may get blocked)")
            url = 'https://shopee.co.id/api/v4/search/search_items'
            params = {
                'by': 'relevancy',
                'limit': limit,
                'match_id': shop_id,
                'newest': offset,
                'order': 'desc',
                'page_type': 'shop',
                'scenario': 'PAGE_OTHERS',
                'version': 2
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Referer': f'https://shopee.co.id/shop/{shop_id}/',
            }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('error') == 0:
            items = data.get('items', [])
            products = []
            
            for item in items:
                item_basic = item.get('item_basic', {})
                
                # Convert price (Shopee price is in cents)
                price = item_basic.get('price', 0) / 100000
                
                # Get main image
                image_id = item_basic.get('image', '')
                image_url = build_shopee_image_url(image_id, shop_id) if image_id else None
                
                product = {
                    'itemid': item_basic.get('itemid'),
                    'shopid': item_basic.get('shopid', shop_id),
                    'name': item_basic.get('name', ''),
                    'price': price,
                    'price_min': item_basic.get('price_min', 0) / 100000,
                    'price_max': item_basic.get('price_max', 0) / 100000,
                    'image': image_url,
                    'images': [build_shopee_image_url(img, shop_id) for img in item_basic.get('images', [])],
                    'stock': item_basic.get('stock', 0),
                    'sold': item_basic.get('sold', 0),
                    'historical_sold': item_basic.get('historical_sold', 0),
                    'liked_count': item_basic.get('liked_count', 0),
                    'rating_star': item_basic.get('item_rating', {}).get('rating_star', 0),
                    'url': build_shopee_product_url(shop_id, item_basic.get('itemid'), item_basic.get('name', '')),
                }
                
                products.append(product)
            
            result = {
                'products': products,
                'total': data.get('total_count', len(products)),
                'has_more': len(items) >= limit
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, result, settings.API_CACHE_TIMEOUT)
            
            return result
        else:
            logger.error(f"Shopee API error: {data.get('error_msg', 'Unknown error')}")
            return {'products': [], 'total': 0, 'has_more': False}
            
    except requests.exceptions.Timeout:
        logger.error("Shopee API timeout")
        logger.info("Using static fallback products")
        return get_fallback_result(limit)
    except requests.exceptions.RequestException as e:
        logger.error(f"Shopee API request error: {e}")
        logger.info("Using static fallback products")
        return get_fallback_result(limit)
    except Exception as e:
        logger.error(f"Unexpected error fetching Shopee products: {e}")
        logger.info("Using static fallback products")
        return get_fallback_result(limit)


def get_fallback_result(limit=50):
    """
    Return static products when API is unavailable
    """
    static_products = get_static_products()
    # Repeat to fill limit
    products = (static_products * ((limit // len(static_products)) + 1))[:limit]
    
    return {
        'products': products,
        'total': len(products),
        'has_more': False,
        'error': 'api_blocked'
    }


def build_shopee_image_url(image_id, shop_id=None):
    """
    Build Shopee CDN image URL from image ID
    
    Args:
        image_id: Shopee image ID
        shop_id: Shop ID (optional, for better caching)
    
    Returns:
        str: Full CDN URL
    """
    if not image_id:
        return None
    
    # Shopee CDN format
    return f'https://cf.shopee.co.id/file/{image_id}'


def build_shopee_product_url(shop_id, item_id, product_name=''):
    """
    Build Shopee product URL
    
    Args:
        shop_id: Shopee shop ID
        item_id: Product item ID
        product_name: Product name (optional, for SEO-friendly URL)
    
    Returns:
        str: Full product URL
    """
    if product_name:
        # Create slug from product name
        slug = product_name.lower().replace(' ', '-')
        return f'https://shopee.co.id/product/{shop_id}/{item_id}?name={slug}'
    return f'https://shopee.co.id/product/{shop_id}/{item_id}'


def format_price(price):
    """
    Format price to Indonesian Rupiah
    
    Args:
        price: Price in numeric format
    
    Returns:
        str: Formatted price string (e.g., "Rp 150.000")
    """
    if price is None:
        return "Rp 0"
    
    return f"Rp {price:,.0f}".replace(',', '.')
