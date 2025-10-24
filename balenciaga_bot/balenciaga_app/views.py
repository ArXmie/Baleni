from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *

# Create your views here.
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

def index(request, category_id):
    categories = Category.objects.all().order_by('category') 
    products = Product.objects.select_related('category').all()  
    images = Product_Image.objects.all()
    return render(request, "index.html", { 'categories': categories, 'products': products, 'images': images, })

