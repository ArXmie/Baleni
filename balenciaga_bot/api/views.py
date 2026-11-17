from decimal import Decimal, InvalidOperation

from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from rest_framework import mixins, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from balenciaga_app.models import (
    Address, Category, Size,
    Product, Product_Image, Size_Product,
    Commission, Commission_Product, Cart, Cart_Product,
)
from .serializers import (
    UserSerializer, AddressSerializer, CategorySerializer, SizeSerializer,
    ProductSerializer, ProductImageSerializer, SizeProductSerializer,
    CommissionSerializer, CommissionProductSerializer, CartItemSerializer,
)


User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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


def cart_response(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    items = cart.items.select_related('product', 'size').order_by('id')
    total = sum(i.product.price * i.amount for i in items)
    return {
        'id': cart.id,
        'items': CartItemSerializer(items, many=True).data,
        'count': sum(i.amount for i in items),
        'total': str(total),
    }


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.none()

    def list(self, request):
        return Response(cart_response(request.user))

    @action(detail=False, methods=['post'], url_path='add')
    def add(self, request):
        product = Product.objects.filter(pk=request.data.get('product')).first()
        if product is None:
            return Response({'detail': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        try:
            amount = int(request.data.get('amount', 1))
        except (TypeError, ValueError):
            amount = 0
        if amount < 1:
            return Response({'detail': 'Неверное количество'}, status=status.HTTP_400_BAD_REQUEST)

        size_name = request.data.get('size') or None
        size = None
        available = Size_Product.objects.filter(product=product).select_related('size')
        if size_name:
            link = available.filter(size__size=size_name).first()
            if link is None:
                return Response({'detail': 'У товара нет такого размера'}, status=status.HTTP_400_BAD_REQUEST)
            size = link.size
        elif available.exists():
            return Response({'detail': 'Выберите размер'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = Cart_Product.objects.get_or_create(
            cart=cart, product=product, size=size, defaults={'amount': amount},
        )
        if not created:
            item.amount += amount
            item.save()
        return Response(cart_response(request.user), status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        Cart_Product.objects.filter(cart__user=request.user).delete()
        return Response(cart_response(request.user))


class CartItemViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        return Cart_Product.objects.filter(cart__user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()
        try:
            amount = int(request.data.get('amount'))
        except (TypeError, ValueError):
            return Response({'detail': 'Неверное количество'}, status=status.HTTP_400_BAD_REQUEST)
        if amount < 1:
            item.delete()
        else:
            item.amount = amount
            item.save()
        return Response(cart_response(request.user))

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(cart_response(request.user))
