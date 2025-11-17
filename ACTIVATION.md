# ✅ AKTIVASI API MODE - Quick Start

## 🚀 Langkah Cepat Aktivasi

### 1. Backup & Replace URLs

**File: Blog/Blog/urls.py**
```python
# Ganti isi file dengan:
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('posting.urls_new')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**File: Blog/posting/urls.py**
```python
# Ganti isi file dengan:
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

### 2. Update Templates

**Rename template files:**
```bash
# Di folder Blog/template/posting/
# Rename atau copy:
mv product_list_api.html product_list.html
mv instagram_api.html instagram.html
```

**Update homepage.html** untuk include template baru jika perlu, atau gunakan yang sudah ada.

### 3. Test Local

```bash
cd Blog
python manage.py runserver
```

**Test URLs:**
- http://127.0.0.1:8000/ - Homepage
- http://127.0.0.1:8000/products/ - Products from Shopee
- http://127.0.0.1:8000/instagram/ - Instagram feed

### 4. Deploy ke Vercel

```bash
git add -A
git commit -m "Activate API mode"
git push origin main
```

Vercel will auto-deploy!

## 🔑 Optional: Set Environment Variables

### Di Vercel Dashboard:

**Settings → Environment Variables → Add:**

1. **SHOPEE_SHOP_ID** (Optional - auto-resolved)
   - Value: (leave empty for auto-resolve from username)

2. **INSTAGRAM_ACCESS_TOKEN** (Optional)
   - Value: Get from Facebook Developers
   - See: UPGRADE_GUIDE.md for instructions

3. **SECRET_KEY** (Recommended for production)
   - Value: Generate new Django secret key
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **DEBUG** (Production)
   - Value: `False`

## 📋 Checklist

- [ ] URLs updated (Blog/urls.py & posting/urls.py)
- [ ] Templates renamed or updated
- [ ] Tested locally
- [ ] Pushed to GitHub
- [ ] Vercel deployed
- [ ] Environment variables set (optional)
- [ ] Tested production URL

## 🎯 Expected Results

✅ **Without Tokens:**
- Shopee products: ✅ Auto-fetch from modelmanis34
- Instagram: ⚠️ Shows profile link fallback

✅ **With Instagram Token:**
- Shopee products: ✅ Auto-fetch
- Instagram: ✅ Shows real feed

## 🐛 Quick Troubleshooting

**Problem: 404 Not Found**
→ Make sure URLs are updated correctly

**Problem: Template Does Not Exist**
→ Rename templates as described in step 2

**Problem: No Products Showing**
→ Check console for API errors
→ Test: https://shopee.co.id/modelmanis34

**Problem: No Instagram Feed**
→ Normal if ACCESS_TOKEN not set
→ Will show profile link instead

## 📞 Support

Lihat file lengkap: **UPGRADE_GUIDE.md** untuk detail technical.

---

**Status: READY TO ACTIVATE** ✅

Just update URLs and you're good to go!
