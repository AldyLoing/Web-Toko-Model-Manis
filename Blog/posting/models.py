from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime

# ✅ Model Kategori Produk
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ✅ Model Produk
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Detail produk
    material = models.CharField(max_length=100, blank=True, verbose_name="Bahan")
    size = models.CharField(max_length=100, blank=True, verbose_name="Ukuran")
    color = models.CharField(max_length=100, blank=True, verbose_name="Warna")
    weight = models.CharField(max_length=50, blank=True, verbose_name="Berat")
    
    # Harga dan stok
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Harga")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stok")
    
    # Link marketplace
    tiktok_url = models.URLField(blank=True, verbose_name="Link Tiktok")
    shopee_url = models.URLField(blank=True, verbose_name="Link Shopee")
    
    # Status produk
    is_best_seller = models.BooleanField(default=False)
    is_new_product = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def main_image(self):
        """Get the main product image"""
        first_image = self.images.first()
        return first_image.image if first_image else None

# ✅ Model Gambar Produk
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


# ✅ Model Banner Slider
class Slide(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    button_text = models.CharField(max_length=50, default="Lihat Produk")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

# ✅ Model Informasi Toko
class StoreInfo(models.Model):
    TYPE_CHOICES = [
        ('about', 'Tentang Toko'),
        ('vision', 'Visi'),
        ('mission', 'Misi'),
        ('story', 'Cerita Brand'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='store_info/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# ✅ Model Kontak Toko
class ContactInfo(models.Model):
    store_name = models.CharField(max_length=100, default="Toko Model Manis")
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    
    # Koordinat untuk peta
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Jam operasional
    operating_hours = models.TextField(blank=True, help_text="Contoh: Senin-Sabtu 09:00-17:00")
    
    # Media sosial
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Marketplace
    tiktok_store_url = models.URLField(blank=True)
    shopee_store_url = models.URLField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return self.store_name

# ✅ Model Pesan Kontak
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"