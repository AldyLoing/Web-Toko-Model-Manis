"""
Instagram API Utilities
Fetch Instagram feed using Instagram Basic Display API
"""
import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def fetch_instagram_feed(access_token=None, limit=12):
    """
    Fetch Instagram media feed
    
    Args:
        access_token: Instagram access token (if None, get from settings)
        limit: Number of posts to fetch
    
    Returns:
        dict: {
            'media': [...],
            'profile_url': str,
            'has_token': bool
        }
    """
    # Get access token
    if not access_token:
        access_token = settings.INSTAGRAM_ACCESS_TOKEN
    
    if not access_token:
        logger.warning("Instagram access token not configured")
        return {
            'media': [],
            'profile_url': settings.INSTAGRAM_PROFILE_URL,
            'has_token': False,
            'error': 'Access token not configured'
        }
    
    # Check cache
    cache_key = f'instagram_feed_{limit}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        url = 'https://graph.instagram.com/me/media'
        params = {
            'fields': 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp',
            'access_token': access_token,
            'limit': limit
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data:
            media_items = []
            
            for item in data['data']:
                media_type = item.get('media_type', 'IMAGE')
                
                # Get appropriate media URL
                if media_type == 'VIDEO':
                    media_url = item.get('thumbnail_url') or item.get('media_url')
                else:
                    media_url = item.get('media_url')
                
                media_item = {
                    'id': item.get('id'),
                    'caption': item.get('caption', ''),
                    'media_type': media_type,
                    'media_url': media_url,
                    'permalink': item.get('permalink', settings.INSTAGRAM_PROFILE_URL),
                    'timestamp': item.get('timestamp', ''),
                }
                
                media_items.append(media_item)
            
            result = {
                'media': media_items,
                'profile_url': settings.INSTAGRAM_PROFILE_URL,
                'has_token': True,
                'count': len(media_items)
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, result, settings.API_CACHE_TIMEOUT)
            
            return result
        else:
            logger.error(f"Instagram API error: {data.get('error', {}).get('message', 'Unknown error')}")
            return {
                'media': [],
                'profile_url': settings.INSTAGRAM_PROFILE_URL,
                'has_token': True,
                'error': data.get('error', {}).get('message', 'API error')
            }
            
    except requests.exceptions.Timeout:
        logger.error("Instagram API timeout")
        return {
            'media': [],
            'profile_url': settings.INSTAGRAM_PROFILE_URL,
            'has_token': True,
            'error': 'API timeout'
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Instagram API request error: {e}")
        return {
            'media': [],
            'profile_url': settings.INSTAGRAM_PROFILE_URL,
            'has_token': True,
            'error': str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching Instagram feed: {e}")
        return {
            'media': [],
            'profile_url': settings.INSTAGRAM_PROFILE_URL,
            'has_token': True,
            'error': str(e)
        }


def truncate_caption(caption, max_length=100):
    """
    Truncate Instagram caption to specified length
    
    Args:
        caption: Full caption text
        max_length: Maximum length
    
    Returns:
        str: Truncated caption with ellipsis if needed
    """
    if not caption:
        return ''
    
    if len(caption) <= max_length:
        return caption
    
    return caption[:max_length].rsplit(' ', 1)[0] + '...'


def get_instagram_profile_info():
    """
    Get basic Instagram profile information
    Returns static info since Basic Display API doesn't provide profile data easily
    """
    return {
        'username': 'modelmanis_rtl',
        'profile_url': settings.INSTAGRAM_PROFILE_URL,
        'display_name': 'Model Manis'
    }
