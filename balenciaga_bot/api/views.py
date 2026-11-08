from decimal import Decimal, InvalidOperation

from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from rest_framework import mixins, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from balenciaga_app.models import (
    Address, Category, Size,
    Product, Product_Image, Size_Product,
    Commission, Commission_Product,
)
from .serializers import (
    UserSerializer, AddressSerializer, CategorySerializer, SizeSerializer,
    ProductSerializer, ProductImageSerializer, SizeProductSerializer,
    CommissionSerializer, CommissionProductSerializer,
)


User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # Только регистрация и вход: список, изменение и удаление пользователей
    # через открытый API недопустимы (в том числе для администратора).
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            first = next(iter(errors.values()))
            message = first[0] if isinstance(first, list) else str(first)
            return Response({'detail': str(message), 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = signing.dumps({'user_id': user.id})
        return Response({'user': UserSerializer(user).data, 'token': token}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        nickname = (request.data.get('nickname') or '').strip()
        password = request.data.get('password') or ''
        user = authenticate(request, username=nickname, password=password)
        if user is None:
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