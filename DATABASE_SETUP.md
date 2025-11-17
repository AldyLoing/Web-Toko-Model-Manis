# Database Setup untuk Vercel

## Masalah
SQLite tidak bisa digunakan di Vercel karena serverless environment tidak memiliki persistent filesystem.

## Solusi 1: Menggunakan Vercel Postgres (Recommended)

### Langkah-langkah:

1. **Buka Vercel Dashboard** → Pilih project Anda → **Storage**

2. **Create Database** → Pilih **Postgres**
   - Pilih region yang dekat dengan pengguna
   - Klik **Create**

3. **Connect to Project**
   - Vercel akan otomatis menambahkan environment variables:
     - `POSTGRES_URL`
     - `POSTGRES_PRISMA_URL`
     - `POSTGRES_URL_NON_POOLING`
     - dan lainnya

4. **Set DATABASE_URL**
   - Di project Settings → Environment Variables
   - Tambahkan: `DATABASE_URL` = nilai dari `POSTGRES_URL`

5. **Redeploy**
   - Vercel akan otomatis redeploy dan menggunakan PostgreSQL

6. **Run Migrations** (via Vercel CLI):
   ```bash
   vercel env pull .env.local
   python Blog/manage.py migrate
   ```

### Biaya
- **Hobby Plan**: $0.25/GB storage per month + $0.25/million rows read
- Free tier tersedia dengan limit tertentu

---

## Solusi 2: Menggunakan External PostgreSQL (Gratis)

### Option A: Neon.tech (Recommended - Free Tier)

1. **Daftar di [neon.tech](https://neon.tech)**
   - Free tier: 3GB storage, 0.5 GB RAM

2. **Create Project**
   - Pilih region
   - Copy connection string

3. **Add to Vercel**
   - Vercel Dashboard → Settings → Environment Variables
   - Key: `DATABASE_URL`
   - Value: `postgresql://[user]:[password]@[host]/[database]?sslmode=require`

### Option B: Supabase (Free Tier)

1. **Daftar di [supabase.com](https://supabase.com)**
   - Free tier: 500MB database, unlimited API requests

2. **Create Project**
   - Settings → Database → Connection string
   - Copy "URI" format

3. **Add to Vercel**
   - Sama seperti Neon di atas

### Option C: Railway.app (Free Trial)

1. **Daftar di [railway.app](https://railway.app)**
   - $5 free credit per month

2. **Create PostgreSQL Database**
   - Copy connection URL

3. **Add to Vercel**
   - Sama seperti di atas

---

## Solusi 3: In-Memory Database (Temporary/Demo Only)

**PERINGATAN**: Data akan hilang setiap kali function restart!

Saat ini project sudah dikonfigurasi untuk menggunakan in-memory SQLite jika tidak ada DATABASE_URL. Ini hanya untuk demo/testing.

### Keterbatasan:
- ❌ Data hilang saat restart
- ❌ Tidak ada persistence
- ❌ Setiap request mungkin dapat database kosong
- ✅ Bagus untuk demo static atau read-only

---

## Quick Setup (Recommended: Neon.tech)

```bash
# 1. Daftar di neon.tech dan buat project

# 2. Copy connection string, contoh:
# postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# 3. Di Vercel Dashboard:
# Settings → Environment Variables → Add
# Name: DATABASE_URL
# Value: [paste connection string]

# 4. Redeploy (otomatis atau manual)

# 5. Run migrations (optional - via local or Vercel CLI)
vercel env pull .env.local
python Blog/manage.py migrate
python Blog/manage.py createsuperuser
```

---

## Testing Local dengan PostgreSQL

Jika ingin test dengan PostgreSQL di local:

```bash
# Install PostgreSQL locally
# Kemudian set environment variable:

# Windows PowerShell:
$env:DATABASE_URL="postgresql://user:password@localhost/dbname"
python Blog/manage.py migrate
python Blog/manage.py runserver

# Windows CMD:
set DATABASE_URL=postgresql://user:password@localhost/dbname
python Blog/manage.py migrate
python Blog/manage.py runserver
```

---

## Current Status

✅ Project sudah dikonfigurasi untuk support:
- PostgreSQL via DATABASE_URL environment variable
- Fallback ke in-memory SQLite untuk demo
- Local development tetap menggunakan SQLite

**Next Step**: Setup PostgreSQL database menggunakan salah satu solusi di atas.
