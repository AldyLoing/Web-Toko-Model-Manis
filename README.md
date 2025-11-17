# 🛍️ Web Toko Model Manis

Website e-commerce untuk Toko Model Manis - **Stateless API-based** menggunakan Django Framework. Website ini menampilkan produk real-time dari Shopee dan Instagram tanpa database.

![Django](https://img.shields.io/badge/Django-5.1.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Deskripsi

Web Toko Model Manis adalah platform showcase modern yang menampilkan produk langsung dari **Shopee API** dan feed dari **Instagram**. Website ini:
- ✅ **Tanpa Database** - Fully stateless, API-first architecture
- ✅ **Real-time Data** - Produk langsung dari Shopee store
- ✅ **Serverless Ready** - Deploy ke Vercel tanpa masalah
- ✅ **Instagram Integration** - Feed Instagram otomatis
- ✅ **Cloudflare Worker Proxy** - Bypass Shopee 403 blocks

## 🚀 Quick Start

### Option 1: With Cloudflare Worker (Recommended)

**Solves Shopee 403 errors permanently!**

See [Cloudflare Worker Setup Guide](cloudflare-worker/README.md) for detailed instructions.

**Quick steps:**
1. Deploy Worker from `cloudflare-worker/shopee-proxy.js`
2. Add `SHOPEE_PROXY` to Vercel environment variables
3. Done! Products load without 403 errors

### Option 2: Without Worker (Fallback Mode)

Website will show placeholder products with links to your Shopee store.

## ✨ Fitur Utama

### 🎯 Fitur API-Based
- **Shopee Products API**: Fetch real-time products from Shopee store
- **Instagram Feed API**: Display Instagram posts automatically
- **Cloudflare Worker Proxy**: Bypass Shopee API restrictions
- **Smart Caching**: 5-minute cache for better performance
- **Graceful Fallback**: Placeholder products if API fails
- **No Database**: Stateless serverless architecture

### 🔧 Technical Features
- **Real-time Product Sync**: Always shows latest Shopee products
- **Instagram Gallery**: Auto-updates from Instagram profile
- **Responsive Design**: Bootstrap 5 mobile-first
- **Static File Serving**: WhiteNoise for production
- **Environment-based Config**: Easy deployment to any platform

## 🛠️ Teknologi yang Digunakan

- **Backend**: Django 5.1.6 (API mode, no database)
- **External APIs**: Shopee API, Instagram Basic Display API
- **Proxy**: Cloudflare Workers (bypasses 403)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Caching**: Django LocMemCache
- **Deployment**: Vercel Serverless
- **Static Files**: WhiteNoise

## 📦 Instalasi

### Prasyarat
- Python 3.10 atau lebih tinggi
- pip (Python package manager)
- Virtual environment (recommended)

### Langkah-langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/AldyLoing/Web-Toko-Model-Manis.git
   cd Web-Toko-Model-Manis
   ```

2. **Buat Virtual Environment**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # Linux/Mac
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Atau install manual:
   ```bash
   pip install django==5.1.6
   pip install pillow==11.3.0
   pip install asgiref==3.8.1
   pip install sqlparse
   ```

4. **Migrasi Database**
   ```bash
   cd Blog
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Buat Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   Ikuti petunjuk untuk membuat username, email, dan password admin.

6. **Jalankan Server Development**
   ```bash
   python manage.py runserver
   ```

7. **Akses Website**
   - Homepage: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`
   - Management Dashboard: `http://127.0.0.1:8000/management/dashboard/`

## 📁 Struktur Project

```
Web-Toko-Model-Manis/
├── Blog/                          # Main project directory
│   ├── Blog/                      # Django project settings
│   │   ├── settings.py           # Konfigurasi project
│   │   ├── urls.py               # URL routing utama
│   │   └── wsgi.py               # WSGI configuration
│   ├── posting/                   # Main application
│   │   ├── models.py             # Database models
│   │   ├── views.py              # View functions
│   │   ├── forms.py              # Form handling
│   │   ├── urls.py               # App URL routing
│   │   ├── admin.py              # Admin configuration
│   │   ├── middleware/           # Custom middleware
│   │   │   └── auto_staff.py    # Auto staff promotion
│   │   ├── management/           # Custom commands
│   │   │   └── commands/
│   │   └── templatetags/         # Custom template tags
│   ├── template/                  # HTML templates
│   │   ├── base.html             # Base template
│   │   ├── posting/              # Public templates
│   │   │   ├── homepage.html    # Homepage
│   │   │   ├── product_list.html
│   │   │   ├── product_detail.html
│   │   │   ├── about_us.html
│   │   │   └── contact.html
│   │   ├── management/           # Admin templates
│   │   │   ├── dashboard.html
│   │   │   ├── products.html
│   │   │   ├── categories.html
│   │   │   └── slider.html
│   │   └── registration/         # Auth templates
│   │       ├── login.html
│   │       └── signup.html
│   ├── static/                    # Static files (CSS, JS, Images)
│   │   ├── css/
│   │   └── img/
│   ├── media/                     # User uploaded files
│   │   ├── products/             # Product images
│   │   ├── categories/           # Category images
│   │   ├── slider/               # Slider images
│   │   └── mitra_logos/          # Partner logos
│   ├── manage.py                 # Django management script
│   └── db.sqlite3                # SQLite database
└── README.md                      # Project documentation
```

## 🗃️ Database Models

### Category
- `name`: Nama kategori
- `slug`: URL-friendly name
- `description`: Deskripsi kategori
- `image`: Gambar kategori
- `is_active`: Status aktif/nonaktif

### Product
- `name`: Nama produk
- `slug`: URL-friendly name
- `category`: Foreign key ke Category
- `description`: Deskripsi lengkap
- `material`: Bahan produk
- `size`: Ukuran produk
- `color`: Warna produk
- `weight`: Berat produk
- `price`: Harga produk
- `stock`: Stok tersedia
- `tiktok_url`: Link TikTok
- `shopee_url`: Link Shopee
- `is_best_seller`: Status best seller
- `is_new_product`: Status produk baru
- `is_featured`: Status featured

### ProductImage
- `product`: Foreign key ke Product
- `image`: File gambar
- `alt_text`: Alternative text
- `is_main`: Status gambar utama
- `order`: Urutan gambar

### Slide
- `title`: Judul slide
- `description`: Deskripsi
- `image`: Gambar banner
- `product`: Foreign key ke Product
- `button_text`: Text tombol
- `is_active`: Status aktif
- `order`: Urutan slide

### ContactInfo
- `store_name`: Nama toko
- `email`: Email kontak
- `phone`: Nomor telepon
- `whatsapp`: Nomor WhatsApp
- `address`: Alamat toko
- Social media links (Instagram, Facebook, TikTok)

## 🎨 Fitur Khusus

### Auto Staff Middleware
Middleware khusus yang otomatis memberikan status staff kepada user yang login, memudahkan akses ke management panel.

### Dynamic Slider
Slider banner yang dapat dikonfigurasi melalui admin panel dengan link langsung ke produk tertentu.

### Marketplace Integration
Setiap produk dapat memiliki link langsung ke TikTok dan Shopee untuk memudahkan pembelian.

### Multiple Image Upload
Mendukung upload multiple gambar untuk setiap produk dengan fitur set main image.

## 🚀 Deployment

### Persiapan untuk Production

1. **Update Settings**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Konfigurasi Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Production**
   - Ubah dari SQLite ke PostgreSQL/MySQL untuk production
   - Update database settings di `settings.py`

4. **Environment Variables**
   - Simpan `SECRET_KEY` di environment variable
   - Gunakan `.env` file untuk konfigurasi sensitif

## 🤝 Kontribusi

Kontribusi sangat diterima! Jika Anda ingin berkontribusi:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 To-Do List

- [ ] Implementasi sistem keranjang belanja
- [ ] Integrasi payment gateway
- [ ] Sistem review dan rating produk
- [ ] Wishlist produk
- [ ] Email notification
- [ ] Search functionality dengan filter advanced
- [ ] Export data produk ke Excel/CSV
- [ ] Multi-language support
- [ ] SEO optimization

## 📄 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👨‍💻 Developer

**Aldy Loing**
- GitHub: [@AldyLoing](https://github.com/AldyLoing)

## 📞 Kontak

Jika Anda memiliki pertanyaan atau saran, silakan hubungi melalui:
- Email: [Your Email]
- WhatsApp: [Your WhatsApp]
- Instagram: [@modelmanis](https://instagram.com/modelmanis)

## 🙏 Acknowledgments

- Django Framework
- Bootstrap
- LineIcons
- Semua kontributor yang telah membantu project ini

---

⭐ Jika project ini bermanfaat, jangan lupa berikan star!

**Made with ❤️ by Aldy Loing**
