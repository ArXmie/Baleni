from decimal import Decimal, InvalidOperation

from django.core import signing
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from balenciaga_app.models import (
    User, Address, Category, Size,
    Product, Product_Image, Size_Product,
    Commission, Commission_Product,
)
from .serializers import (
    UserSerializer, AddressSerializer, CategorySerializer, SizeSerializer,
    ProductSerializer, ProductImageSerializer, SizeProductSerializer,
    CommissionSerializer, CommissionProductSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        nickname = (request.data.get('nickname') or '').strip()
        if User.objects.filter(nickname__iexact=nickname).exists():
            return Response({'detail': 'Никнейм уже занят'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        from balenciaga_app.views import check_password
        nickname = (request.data.get('nickname') or '').strip()
        password = request.data.get('password') or ''
        user = User.objects.filter(nickname=nickname).first()
        if not user or not check_password(password, user.password):
            return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        token = signing.dumps({'user_id': user.id})
        return Response({'user': UserSerializer(user).data, 'token': token})


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'desc', 'article_number']
    ordering_fields = ['price', 'name', 'amount']

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        for key, lookup in (('price__gte', 'price__gte'), ('price__lte', 'price__lte')):
            value = params.get(key)
            if value not in (None, ''):
                try:
                    qs = qs.filter(**{lookup: Decimal(value)})
                except (InvalidOperation, ValueError):
                    pass
        category = params.get('category')
        if category and category.isdigit():
            qs = qs.filter(category_id=int(category))
        return qs


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = Product_Image.objects.all()
    serializer_class = ProductImageSerializer


class SizeProductViewSet(viewsets.ModelViewSet):
    queryset = Size_Product.objects.all()
    serializer_class = SizeProductSerializer


class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class CommissionProductViewSet(viewsets.ModelViewSet):
    queryset = Commission_Product.objects.all()
    serializer_class = CommissionProductSerializer