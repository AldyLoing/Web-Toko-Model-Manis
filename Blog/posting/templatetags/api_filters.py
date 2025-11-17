"""
Custom template tags for Model Manis
"""
from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='format_price')
def format_price(value):
    """
    Format number to Indonesian Rupiah
    Usage: {{ price|format_price }}
    """
    try:
        value = float(value)
        return f"Rp {value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return "Rp 0"


@register.filter(name='truncate_text')
def truncate_text(text, length=100):
    """
    Truncate text to specified length
    Usage: {{ caption|truncate_text:150 }}
    """
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return text[:length].rsplit(' ', 1)[0] + '...'


@register.filter(name='shopee_image')
def shopee_image(image_id):
    """
    Convert Shopee image ID to CDN URL
    Usage: {{ image_id|shopee_image }}
    """
    if not image_id:
        return ''
    return f'https://cf.shopee.co.id/file/{image_id}'


@register.simple_tag
def shopee_product_url(shop_id, item_id, product_name=''):
    """
    Build Shopee product URL
    Usage: {% shopee_product_url shopid itemid name %}
    """
    if product_name:
        slug = product_name.lower().replace(' ', '-')
        return f'https://shopee.co.id/product/{shop_id}/{item_id}?name={slug}'
    return f'https://shopee.co.id/product/{shop_id}/{item_id}'


@register.simple_tag
def get_setting(name):
    """
    Get Django setting value
    Usage: {% get_setting 'SHOPEE_STORE_URL' %}
    """
    return getattr(settings, name, '')


@register.filter(name='format_number')
def format_number(value):
    """
    Format number with thousand separators
    Usage: {{ sold|format_number }}
    """
    try:
        value = int(value)
        return f"{value:,}".replace(',', '.')
    except (ValueError, TypeError):
        return "0"


@register.filter(name='rating_stars')
def rating_stars(rating):
    """
    Convert rating to star display
    Usage: {{ rating|rating_stars }}
    """
    try:
        rating = float(rating)
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        stars = '★' * full_stars
        if half_star:
            stars += '☆'
        stars += '☆' * empty_stars
        
        return f"{stars} ({rating:.1f})"
    except (ValueError, TypeError):
        return "☆☆☆☆☆"


@register.inclusion_tag('posting/components/product_card.html')
def product_card(product):
    """
    Render product card component
    Usage: {% product_card product %}
    """
    return {'product': product}


@register.filter(name='instagram_type_icon')
def instagram_type_icon(media_type):
    """
    Get icon class for Instagram media type
    Usage: {{ media_type|instagram_type_icon }}
    """
    icons = {
        'IMAGE': 'lni lni-image',
        'VIDEO': 'lni lni-video',
        'CAROUSEL_ALBUM': 'lni lni-gallery',
    }
    return icons.get(media_type, 'lni lni-image')
