from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, Category, ProductImage, Slide, 
    StoreInfo, ContactInfo, ContactMessage
)

# Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main', 'order')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order')

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'product_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_best_seller', 'is_new_product', 'created_at')
    list_filter = ('category', 'is_active', 'is_best_seller', 'is_new_product', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Product Details', {
            'fields': ('material', 'size', 'color', 'weight')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Marketplace Links', {
            'fields': ('tiktok_url', 'shopee_url')
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_best_seller', 'is_new_product', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new product
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'created_by')

# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_main', 'order', 'image_preview')
    list_filter = ('is_main', 'product__category')
    search_fields = ('product__name', 'alt_text')
    ordering = ('product', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

# Slide Admin
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'image', 'product', 'button_text')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

# Store Info Admin
@admin.register(StoreInfo)
class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'updated_at')
    list_filter = ('type',)
    search_fields = ('title', 'content')
    
    fieldsets = (
        ('Content', {
            'fields': ('type', 'title', 'content', 'image')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('updated_at',)

# Contact Info Admin
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'phone', 'email', 'updated_at')
    
    fieldsets = (
        ('Store Information', {
            'fields': ('store_name', 'phone', 'whatsapp', 'email', 'address', 'operating_hours')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'description': 'Enter coordinates for map display'
        }),
        ('Social Media', {
            'fields': ('instagram_url', 'facebook_url', 'youtube_url')
        }),
        ('Marketplace', {
            'fields': ('tiktok_store_url', 'shopee_store_url')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('updated_at',)

# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Details', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"

# Customize admin site
admin.site.site_header = "Toko Model Manis Admin"
admin.site.site_title = "Toko Model Manis"
admin.site.index_title = "Dashboard Manajemen Toko"
