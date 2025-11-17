# 🚀 Upgrade Guide: Database-Free API Version

## Apa Yang Berubah?

Project ini telah di-upgrade menjadi **stateless API-based application** tanpa database. Semua data produk dan Instagram feed diambil secara real-time dari API eksternal.

### ✅ Perubahan Utama:

1. **Tidak Ada Database**
   - SQLite, PostgreSQL, dan semua database dependency dihapus
   - Menggunakan `dummy` database engine
   - Data diambil langsung dari Shopee dan Instagram API

2. **Shopee API Integration**
   - Fetch produk dari toko Shopee: https://shopee.co.id/modelmanis34
   - Real-time product data (nama, harga, gambar, stok, terjual)
   - Auto-convert Shopee image IDs ke CDN URLs
   - Built-in caching (5 menit) untuk performa

3. **Instagram API Integration**
   - Fetch feed dari Instagram: https://www.instagram.com/modelmanis_rtl/
   - Display media (gambar/video), caption, dan permalink
   - Fallback ke profile link jika access token tidak tersedia

4. **New File Structure**
   ```
   Blog/posting/
   ├── utils/
   │   ├── shopee_api.py       # Shopee API utilities
   │   └── instagram_api.py    # Instagram API utilities
   ├── templatetags/
   │   └── api_filters.py      # Template filters untuk API data
   ├── views_new.py            # New views tanpa database
   └── urls_new.py             # New URL configuration
   ```

## 🔧 Setup & Configuration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies minimal:
- Django==5.1.6
- whitenoise==6.8.2
- requests==2.32.3
- Pillow==11.3.0

### 2. Environment Variables

Buat file `.env` atau set environment variables:

```bash
# Optional: Shopee Shop ID (auto-resolve jika tidak diset)
SHOPEE_SHOP_ID=

# Optional: Instagram Access Token
INSTAGRAM_ACCESS_TOKEN=

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 3. Update URLs

Ganti file URLs untuk menggunakan versi baru:

**Blog/Blog/urls.py:**
```python
from django.urls import path, include

urlpatterns = [
    path('', include('posting.urls_new')),
]
```

**Blog/posting/urls.py:**
```python
from django.urls import path
from . import views_new as views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('instagram/', views.instagram_gallery, name='instagram_gallery'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
]
```

### 4. Update Templates

Gunakan template baru yang sudah dibuat:
- `base_api.html` - Base template
- `posting/product_list_api.html` - Product listing
- `posting/instagram_api.html` - Instagram gallery

Atau update existing templates dengan:
```django
{% load api_filters %}

<!-- Format price -->
{{ product.price|format_price }}

<!-- Truncate text -->
{{ product.name|truncate_text:60 }}

<!-- Format numbers -->
{{ product.sold|format_number }}
```

### 5. Run Server

```bash
cd Blog
python manage.py runserver
```

**TIDAK PERLU** migrations karena tidak ada database!

## 📖 API Documentation

### Shopee API Functions

```python
from posting.utils.shopee_api import fetch_shopee_products, format_price

# Fetch products
data = fetch_shopee_products(limit=50, offset=0)
products = data['products']
total = data['total']

# Format price
formatted = format_price(150000)  # "Rp 150.000"
```

### Instagram API Functions

```python
from posting.utils.instagram_api import fetch_instagram_feed

# Fetch feed
data = fetch_instagram_feed(limit=12)
media = data['media']
profile_url = data['profile_url']
```

## 🔑 Getting Instagram Access Token

### Option 1: Instagram Basic Display API

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create App → Type: Consumer
3. Add Instagram Basic Display
4. Configure Instagram App
5. Add Test User (your Instagram account)
6. Generate Access Token
7. Copy token to environment variable

### Option 2: Fallback (No Token)

Jika tidak ada token, website akan:
- Menampilkan link ke profile Instagram
- Memberikan pesan user-friendly
- Tidak error/crash

## ⚡ Caching

Built-in caching untuk mencegah throttling:
- Cache duration: 5 menit (300 seconds)
- Configurable via `API_CACHE_TIMEOUT` in settings
- Uses Django's cache framework

## 🚀 Deploy to Vercel

Project sudah configured untuk Vercel:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Upgrade to API-based stateless app"
   git push origin main
   ```

2. **Deploy di Vercel**
   - Import project dari GitHub
   - Framework: Other
   - Build Command: (leave empty)
   - No database needed!

3. **Set Environment Variables** (Optional)
   - `SHOPEE_SHOP_ID`
   - `INSTAGRAM_ACCESS_TOKEN`
   - `SECRET_KEY`
   - `DEBUG=False`

## 🎯 Features

✅ **Tanpa Database** - Fully stateless
✅ **Real-time Data** - Langsung dari API
✅ **Auto Caching** - Performa optimal
✅ **Error Handling** - User-friendly messages
✅ **Responsive Design** - Mobile-friendly
✅ **SEO Friendly** - Product URLs & metadata
✅ **Lazy Loading** - Optimized images
✅ **Vercel Ready** - Deploy-ready configuration

## 📝 Template Tags Available

```django
{% load api_filters %}

<!-- Price formatting -->
{{ price|format_price }}

<!-- Text truncation -->
{{ text|truncate_text:100 }}

<!-- Number formatting -->
{{ number|format_number }}

<!-- Shopee image URL -->
{{ image_id|shopee_image }}

<!-- Shopee product URL -->
{% shopee_product_url shopid itemid name %}

<!-- Get settings -->
{% get_setting 'SHOPEE_STORE_URL' %}
```

## 🐛 Troubleshooting

### Shopee API tidak return data

1. Check apakah `SHOPEE_SHOP_ID` sudah correct
2. Coba akses manual: `https://shopee.co.id/modelmanis34`
3. Check logs untuk error details

### Instagram feed kosong

1. Pastikan `INSTAGRAM_ACCESS_TOKEN` valid
2. Token expired? Generate baru
3. Fallback mode akan show profile link

### Cache issues

```python
# Clear cache
from django.core.cache import cache
cache.clear()
```

## 📊 Performance

- **Cold start**: ~2-3 seconds (API fetch)
- **Cached**: <100ms
- **No database queries**: ✅
- **Scalable**: Serverless-ready

## 🔄 Migration from Old Version

1. Backup old project
2. Pull latest code
3. Update URLs (see step 3 above)
4. Update templates or use new ones
5. No migrations needed!
6. Test locally
7. Deploy

---

**Made with ❤️ for Model Manis**
Stateless • API-First • Serverless Ready
