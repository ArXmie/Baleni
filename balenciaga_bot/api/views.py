from rest_framework import viewsets, filters

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