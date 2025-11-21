from django.shortcuts import render, HttpResponse, get_object_or_404
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
    return render(request, "search.html")

