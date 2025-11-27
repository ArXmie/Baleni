from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import *

# Create your views here.

# 127.0.0.1:8000/mul/?a=5&b=5
def root(request):
    first_compoud = float(request.GET.get('a', 0))
    second_compoud = float(request.GET.get('b', 0))
    result = first_compoud + second_compoud

    return HttpResponse(str(result))

def mul(request):
    first_compoud = float(request.GET.get('a', 0))
    second_compoud = float(request.GET.get('b', 0))
    result = first_compoud - second_compoud

    return HttpResponse(str(result))

def umnoj(request):
    first_compoud = float(request.GET.get('a', 0))
    second_compoud = float(request.GET.get('b', 0))
    result = first_compoud * second_compoud

    return HttpResponse(str(result))

def delenie(request):
    first_compoud = float(request.GET.get('a', 0))
    second_compoud = float(request.GET.get('b', 0))
    result = first_compoud / second_compoud

    return HttpResponse(str(result))

def index(request):
    categories = Category.objects.all()
    data = []

    for category in categories:
        products = category.product_set.all()[:2]
        data.append({'category': category, 'products': products}) 
    images = Product_Image.objects.all()
    return render(request, "main-catalog.html", { 'data': data })

def template_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = Product_Image.objects.filter(product=product)
    similar = Product.objects.filter(category=product.category).exclude(id=product_id)[:3]
    size = Size_Product.objects.filter(product=product)

    context = {
        'product': product,
        'images': images,
        'similar': similar,
        'sizes': size,
    }
    return render(request, "template_product.html", context)

def search(request):
    query = request.GET.get('q', '').strip()
    price_from = request.GET.get('price_from', '')
    price_to = request.GET.get('price_to', '')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
            )
        
    if price_from:
        products = products.filter(price__gte=float(price_from))
    if price_to:
        products = products.filter(price__lte=float(price_to))

    products_with_images = []
    for product in products:
        first_image = Product_Image.objects.filter(product=product).first()
        products_with_images.append({
            'product': product,
            'image': first_image
        })

    context = {
        'query': query,
        'products': products_with_images,
        'count': products.count(),
        'price_from': price_from,
        'price_to': price_to
    }
    return render(request, "search.html", context)

def search_api(request):
    """API для AJAX автодополнения"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    # Поиск товаров
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    )[:10]
    
    results = []
    for product in products:
        first_image = Product_Image.objects.filter(product=product).first()
        
        results.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image': first_image.image if first_image else None,
            'url': f'/product/{product.id}/'
        })
    
    return JsonResponse({'results': results})
