# Panduan Deployment ke Vercel

Project ini telah dikonfigurasi untuk deployment ke Vercel. Ikuti langkah-langkah berikut:

## Persiapan

1. **Buat akun Vercel** (jika belum punya) di [vercel.com](https://vercel.com)
2. **Install Vercel CLI** (opsional):
   ```bash
   npm install -g vercel
   ```

## Cara Deploy

### Metode 1: Melalui Dashboard Vercel (Recommended)

1. Login ke [vercel.com](https://vercel.com)
2. Klik **"Add New Project"**
3. Import repository GitHub Anda: `https://github.com/AldyLoing/Web-Toko-Model-Manis.git`
4. Konfigurasi project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `bash build_files.sh`
   - **Output Directory**: Leave empty
5. Tambahkan **Environment Variables** (opsional):
   - `SECRET_KEY`: Generate secret key baru untuk production
   - `DEBUG`: Set ke `False` untuk production
6. Klik **"Deploy"**

### Metode 2: Melalui Vercel CLI

```bash
# Login ke Vercel
vercel login

# Deploy project
cd "e:\Orders\Project\Web Model Manis"
vercel

# Atau deploy langsung ke production
vercel --prod
```

## Environment Variables (Opsional)

Untuk keamanan lebih baik, set environment variables di Vercel Dashboard:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
```

Generate SECRET_KEY baru dengan:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## File yang Telah Dikonfigurasi

- ✅ `vercel.json` - Konfigurasi deployment Vercel
- ✅ `build_files.sh` - Script build untuk collect static files
- ✅ `.vercelignore` - File yang diabaikan saat deployment
- ✅ `Blog/Blog/settings.py` - Updated untuk production (WhiteNoise, ALLOWED_HOSTS, dll)
- ✅ `Blog/Blog/wsgi.py` - Configured untuk Vercel
- ✅ `requirements.txt` - Dependencies termasuk whitenoise

## Catatan Penting

1. **Database**: Project ini menggunakan SQLite. Untuk production, pertimbangkan menggunakan database eksternal seperti PostgreSQL atau MySQL
2. **Media Files**: File upload (media) tidak akan persisten di Vercel. Gunakan storage eksternal seperti AWS S3, Cloudinary, atau Vercel Blob
3. **Static Files**: Dihandle oleh WhiteNoise, akan dikumpulkan otomatis saat build

## Troubleshooting

### Jika deployment gagal:

1. **Check build logs** di Vercel Dashboard
2. **Pastikan semua dependencies** ada di `requirements.txt`
3. **Verifikasi Python version**: Vercel menggunakan Python 3.9 (dapat diubah di `vercel.json`)
4. **Check ALLOWED_HOSTS**: Update dengan domain Vercel Anda

### Error "Module not found":

Pastikan semua import path benar dan dependencies sudah ada di `requirements.txt`

### Static files tidak muncul:

1. Check apakah `collectstatic` berhasil di build logs
2. Verifikasi `STATIC_ROOT` dan `STATIC_URL` di settings.py

## Setelah Deployment

1. Akses URL yang diberikan oleh Vercel (contoh: `https://your-project.vercel.app`)
2. Test semua fungsi website
3. Jika menggunakan custom domain, configure di Vercel Dashboard > Settings > Domains

## Update Project

Setiap kali Anda push ke branch `main` di GitHub, Vercel akan otomatis deploy ulang:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

## Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Django on Vercel Guide](https://vercel.com/docs/frameworks/django)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
