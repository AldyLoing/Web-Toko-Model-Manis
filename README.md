# 🛍️ Web Toko Model Manis

Website e-commerce untuk Toko Model Manis yang dibangun menggunakan Django Framework. Website ini menampilkan produk-produk kreatif dengan fitur manajemen yang lengkap dan integrasi marketplace.

![Django](https://img.shields.io/badge/Django-5.1.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Deskripsi

Web Toko Model Manis adalah platform e-commerce yang dirancang untuk menampilkan dan mengelola produk-produk kreatif. Website ini dilengkapi dengan:
- Katalog produk dengan kategori
- Slider banner dinamis
- Detail produk lengkap dengan gambar
- Integrasi link marketplace (TikTok & Shopee)
- Dashboard admin untuk manajemen produk
- Sistem informasi toko dan mitra

## ✨ Fitur Utama

### 🎯 Fitur Pengunjung
- **Homepage dengan Slider**: Banner dinamis untuk menampilkan produk unggulan
- **Katalog Produk**: Tampilan produk dengan filter kategori
- **Detail Produk**: Informasi lengkap produk termasuk material, ukuran, warna, dan harga
- **Link Marketplace**: Integrasi langsung ke TikTok dan Shopee
- **Tentang Kami**: Informasi lengkap tentang toko
- **Kontak**: Form kontak untuk komunikasi dengan toko

### 🔧 Fitur Admin/Management
- **Dashboard Management**: Panel kontrol untuk mengelola toko
- **Manajemen Produk**: CRUD (Create, Read, Update, Delete) produk
- **Manajemen Kategori**: Organisasi produk berdasarkan kategori
- **Manajemen Slider**: Kontrol banner slider homepage
- **Upload Gambar**: Multiple image upload untuk produk
- **Informasi Toko**: Update informasi kontak dan sosial media
- **Auto Staff Middleware**: Otomatis promote user menjadi staff

## 🛠️ Teknologi yang Digunakan

- **Backend**: Django 5.1.6
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Image Processing**: Pillow 11.3.0
- **Static Files**: Django Static Files
- **Media Storage**: Django Media Files

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
