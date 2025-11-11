from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.text import slugify
from .models import (
    Product, Category, ProductImage, Slide, StoreInfo, 
    ContactInfo, ContactMessage
)
from .forms import ContactMessageForm

def fix_category_slugs_view(request):
    """Temporary view to fix category slugs"""
    if request.user.is_staff:
        categories = Category.objects.filter(slug__in=['', None])
        fixed_count = 0
        
        for category in categories:
            category.slug = slugify(category.name)
            category.save()
            fixed_count += 1
        
        categories_empty_slug = Category.objects.filter(slug='')
        for category in categories_empty_slug:
            category.slug = slugify(category.name)
            category.save()
            fixed_count += 1
            
        return JsonResponse({
            'success': True, 
            'message': f'Fixed {fixed_count} category slugs',
            'categories': list(Category.objects.values('id', 'name', 'slug'))
        })
    else:
        return JsonResponse({'success': False, 'message': 'Access denied'})

def homepage(request):
    """Homepage with banner slider, categories, and featured products"""
    slides = Slide.objects.filter(is_active=True).order_by('order')
    categories = Category.objects.all()[:6]  # Show first 6 categories
    best_sellers = Product.objects.filter(is_featured=True, is_active=True)[:8]
    new_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    store_info = StoreInfo.objects.first()
    
    context = {
        'slides': slides,
        'categories': categories,
        'best_sellers': best_sellers,
        'new_products': new_products,
        'store_info': store_info,
    }
    return render(request, 'posting/homepage.html', context)

def product_detail(request, slug):
    """Product detail page with images, specs, and marketplace links"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = ProductImage.objects.filter(product=product)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'images': images,
        'related_products': related_products,
    }
    return render(request, 'posting/product_detail.html', context)

def product_list(request):
    """All products with filtering, sorting, and search"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Sort options
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'current_category': category_id,
        'current_sort': sort_by,
    }
    return render(request, 'posting/product_list.html', context)

def products_by_category(request, slug):
    """Products filtered by specific category"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Sort options
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products,
        'current_sort': sort_by,
    }
    return render(request, 'posting/products_by_category.html', context)

def category_list(request):
    """List all categories"""
    categories = Category.objects.all().order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'posting/category_list.html', context)

def about_us(request):
    """About us page with store info and marketplace links"""
    store_info = StoreInfo.objects.first()
    contact_info = ContactInfo.objects.first()
    
    context = {
        'store_info': store_info,
        'contact_info': contact_info,
    }
    return render(request, 'posting/about_us.html', context)

def contact(request):
    """Contact page with form, WhatsApp, and map"""
    contact_info = ContactInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pesan Anda berhasil dikirim! Kami akan segera menghubungi Anda.')
            return redirect('contact')
    else:
        form = ContactMessageForm()
    
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'posting/contact.html', context)

def search_products(request):
    """AJAX search for products"""
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products_qs = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )[:10]  # Limit to 10 results for AJAX
        
        products = [{
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'price': str(product.price),
            'image': product.image.url if product.image else '',
        } for product in products_qs]
    
    return JsonResponse({'products': products})


# ============================================
# MANAGEMENT VIEWS (Admin Frontend)
# ============================================

@login_required
def manage_dashboard(request):
    """Dashboard utama untuk management"""
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_slides': Slide.objects.count(),
        'recent_products': Product.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    return render(request, 'management/dashboard.html', context)

@login_required
def manage_products(request):
    """Kelola produk"""
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 10)  # 10 produk per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'management/products.html', {
        'page_obj': page_obj,
        'products': page_obj
    })

@login_required
def add_product(request):
    """Tambah produk baru"""
    if request.method == 'POST':
        # Proses form tambah produk
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        category_id = request.POST.get('category')
        tiktok_url = request.POST.get('tiktok_url', '')
        shopee_url = request.POST.get('shopee_url', '')
        image = request.FILES.get('image')
        
        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=int(stock) if stock else 0,
                category=category,
                tiktok_url=tiktok_url,
                shopee_url=shopee_url,
                slug=slugify(name)
            )
            
            # Handle product image if uploaded
            if image:
                from .models import ProductImage
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_main=True,
                    order=1
                )
            
            messages.success(request, f'🛍️ Produk "{product.name}" berhasil ditambahkan ke kategori {category.name}!')
            return redirect('manage_products')
        except Exception as e:
            messages.error(request, f'❌ Gagal menambahkan produk: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'management/add_product.html', {'categories': categories})

@login_required
def edit_product(request, id):
    """Edit produk"""
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        # Update produk
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        product.stock = int(stock) if stock else 0
        product.category_id = request.POST.get('category')
        product.tiktok_url = request.POST.get('tiktok_url', '')
        product.shopee_url = request.POST.get('shopee_url', '')
        product.slug = slugify(product.name)
        
        # Handle product image if uploaded
        if request.FILES.get('image'):
            from .models import ProductImage
            # Remove old main image if exists
            old_main_image = product.images.filter(is_main=True).first()
            if old_main_image:
                old_main_image.delete()
            
            # Add new main image
            ProductImage.objects.create(
                product=product,
                image=request.FILES.get('image'),
                is_main=True,
                order=1
            )
        
        try:
            product.save()
            messages.success(request, f'✅ Produk "{product.name}" berhasil diperbarui!')
            return redirect('manage_products')
        except Exception as e:
            messages.error(request, f'❌ Gagal memperbarui produk: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'management/edit_product.html', {
        'product': product,
        'categories': categories
    })

@login_required
def delete_product(request, id):
    """Hapus produk"""
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Produk "{product_name}" berhasil dihapus!')
        return redirect('manage_products')
    
    return render(request, 'management/delete_product.html', {'product': product})

@login_required
def manage_categories(request):
    """Kelola kategori"""
    categories = Category.objects.all().order_by('name')
    return render(request, 'management/categories.html', {'categories': categories})

@login_required
def add_category(request):
    """Tambah kategori baru"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        
        try:
            # Generate slug dari nama
            slug = slugify(name)
            
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                image=image
            )
            messages.success(request, f'🎉 Kategori "{category.name}" berhasil ditambahkan! Anda dapat mulai menambahkan produk ke kategori ini.')
            return redirect('manage_categories')
        except Exception as e:
            messages.error(request, f'❌ Gagal menambahkan kategori: {str(e)}')
    
    return render(request, 'management/add_category.html')

@login_required
def edit_category(request, id):
    """Edit kategori"""
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        old_name = category.name
        category.name = request.POST.get('name')
        category.description = request.POST.get('description', '')
        
        # Update slug jika nama berubah
        if old_name != category.name:
            category.slug = slugify(category.name)
        
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        
        try:
            category.save()
            messages.success(request, f'✅ Kategori "{category.name}" berhasil diperbarui!')
            return redirect('manage_categories')
        except Exception as e:
            messages.error(request, f'❌ Gagal memperbarui kategori: {str(e)}')
    
    return render(request, 'management/edit_category.html', {'category': category})

@login_required
def manage_slider(request):
    """Kelola slider homepage"""
    slides = Slide.objects.all().order_by('order')
    return render(request, 'management/slider.html', {'slides': slides})

@login_required
def add_slide(request):
    """Tambah slide baru"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        button_text = request.POST.get('button_text', 'Lihat Produk')
        product_id = request.POST.get('product')
        order = request.POST.get('order', 1)
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        try:
            product = None
            if product_id:
                product = Product.objects.get(id=product_id)
            
            slide = Slide.objects.create(
                title=title,
                description=description,
                button_text=button_text,
                product=product,
                order=order,
                is_active=is_active,
                image=image
            )
            messages.success(request, f'🎉 Slide "{slide.title}" berhasil ditambahkan!')
            return redirect('manage_slider')
        except Exception as e:
            messages.error(request, f'❌ Gagal menambahkan slide: {str(e)}')
    
    products = Product.objects.filter(is_active=True)
    return render(request, 'management/add_slide.html', {'products': products})

@login_required
def manage_store_info(request):
    """Kelola informasi toko"""
    # Get or create different types of store info
    about_info, created = StoreInfo.objects.get_or_create(
        type='about',
        defaults={'title': 'Tentang Toko Model Manis', 'content': ''}
    )
    vision_info, created = StoreInfo.objects.get_or_create(
        type='vision',
        defaults={'title': 'Visi Kami', 'content': ''}
    )
    mission_info, created = StoreInfo.objects.get_or_create(
        type='mission',
        defaults={'title': 'Misi Kami', 'content': ''}
    )
    
    # Get contact info
    contact_info, created = ContactInfo.objects.get_or_create(
        id=1,
        defaults={
            'store_name': 'Toko Model Manis',
            'phone': '',
            'whatsapp': '',
            'email': '',
            'address': ''
        }
    )
    
    if request.method == 'POST':
        try:
            # Update about info
            about_info.title = request.POST.get('about_title', about_info.title)
            about_info.content = request.POST.get('about_content', about_info.content)
            if request.FILES.get('about_image'):
                about_info.image = request.FILES.get('about_image')
            about_info.save()
            
            # Update vision
            vision_info.title = request.POST.get('vision_title', vision_info.title)
            vision_info.content = request.POST.get('vision_content', vision_info.content)
            vision_info.save()
            
            # Update mission
            mission_info.title = request.POST.get('mission_title', mission_info.title)
            mission_info.content = request.POST.get('mission_content', mission_info.content)
            mission_info.save()
            
            # Update contact info
            contact_info.store_name = request.POST.get('store_name', contact_info.store_name)
            contact_info.phone = request.POST.get('phone', contact_info.phone)
            contact_info.whatsapp = request.POST.get('whatsapp', contact_info.whatsapp)
            contact_info.email = request.POST.get('email', contact_info.email)
            contact_info.address = request.POST.get('address', contact_info.address)
            contact_info.operating_hours = request.POST.get('operating_hours', contact_info.operating_hours)
            contact_info.instagram_url = request.POST.get('instagram_url', contact_info.instagram_url)
            contact_info.facebook_url = request.POST.get('facebook_url', contact_info.facebook_url)
            contact_info.tiktok_store_url = request.POST.get('tiktok_store_url', contact_info.tiktok_store_url)
            contact_info.shopee_store_url = request.POST.get('shopee_store_url', contact_info.shopee_store_url)
            contact_info.save()
            
            messages.success(request, '✅ Informasi toko berhasil diperbarui!')
            return redirect('manage_store_info')
        except Exception as e:
            messages.error(request, f'❌ Gagal memperbarui informasi: {str(e)}')
    
    return render(request, 'management/store_info.html', {
        'about_info': about_info,
        'vision_info': vision_info,
        'mission_info': mission_info,
        'contact_info': contact_info
    })