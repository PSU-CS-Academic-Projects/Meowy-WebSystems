from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Q
from .models import Category, Product, ProductVariant
import json

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    
    # Annotate products with their minimum variant price for sorting
    products = Product.objects.annotate(min_price=Min('variants__price'))
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) | 
            Q(description__icontains=query)
        )
        
    # Sorting functionality
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('min_price')
    elif sort == 'price_desc':
        products = products.order_by('-min_price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
        
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'sort': sort,
        'query': query,
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    variants = product.variants.all()
    
    # Build list of variant choices for JavaScript dynamic display
    variants_data = []
    for variant in variants:
        variants_data.append({
            'id': variant.id,
            'flavor': variant.flavor,
            'weight': variant.weight,
            'price': str(variant.price),
            'stock': variant.stock,
        })
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'variants': variants,
        'variants_json': json.dumps(variants_data),
    })
