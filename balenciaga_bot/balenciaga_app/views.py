from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
import hashlib
from django.http import JsonResponse
from django.db.models import Q
from .models import *

def make_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hashlib.sha256(password.encode()).hexdigest() == hashed

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
            Q(name__icontains=query) | Q(desc__icontains=query)
        )
    
    if price_from:
        try:
            products = products.filter(price__gte=float(price_from))
        except ValueError:
            pass
    
    if price_to:
        try:
            products = products.filter(price__lte=float(price_to))
        except ValueError:
            pass

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
    
    if request.session.get('user_id'):
        context['nickname'] = request.session.get('nickname')
        return render(request, "search-logged.html", context)
    else:
        return render(request, "search.html", context)

def catalog_logged(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    categories = Category.objects.all()
    data = []

    for category in categories:
        products = category.product_set.all()[:2]
        data.append({'category': category, 'products': products})
    images = Product_Image.objects.all()

    return render(request, 'main-catalog-logged.html', {
        'data': data, 
        'nickname': request.session.get('nickname'),
    })


def login_view(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(nickname=nickname)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['nickname'] = user.nickname
                return redirect('catalog_logged')
            else:
                return render(request, 'login.html', {'error': 'Неверный пароль'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Пользователь не найден'})

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'error': 'Пароли не совпадают'})

        if len(password) < 6:
            return render(request, 'register.html', {'error': 'Пароль минимум 6 символов'})

        if User.objects.filter(nickname=nickname).exists():
            return render(request, 'register.html', {'error': 'Никнейм уже занят'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email уже используется'})

        user = User.objects.create(
            nickname=nickname,
            email=email,
            telephone=telephone,
            password=make_password(password),
        )
        request.session['user_id'] = user.id
        request.session['nickname'] = user.nickname
        return redirect('catalog_logged')

    return render(request, 'register.html')
    

def logout_view(request):
    request.session.flush()
    return redirect('login')
