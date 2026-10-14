from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from balenciaga_app import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'nickname', 'email', 'telephone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        from balenciaga_app.views import make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        from balenciaga_app.views import make_password
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class AddressSerializer(ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SizeSerializer(ModelSerializer):
    class Meta:
        model = models.Size
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = models.Product_Image
        fields = ['id', 'product', 'image']


class SizeProductSerializer(ModelSerializer):
    size_name = CharField(source='size.size', read_only=True)
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = models.Size_Product
        fields = ['id', 'size', 'product', 'size_name', 'product_name']


class ProductSerializer(ModelSerializer):
    category_name = CharField(source='category.category', read_only=True)
    images = ProductImageSerializer(source='product_image_set', many=True, read_only=True)
    sizes = SerializerMethodField()

    def get_sizes(self, obj):
        return [sp.size.size for sp in obj.size_product_set.select_related('size')]

    class Meta:
        model = models.Product
        fields = [
            'id', 'name', 'desc', 'price', 'category', 'category_name',
            'amount', 'article_number', 'images', 'sizes',
        ]


class CommissionProductSerializer(ModelSerializer):
    product_name = CharField(source='product.name', read_only=True)

    class Meta:
        model = models.Commission_Product
        fields = ['id', 'commission', 'product', 'product_name', 'amount', 'price']


class CommissionSerializer(ModelSerializer):
    user_nickname = CharField(source='user.nickname', read_only=True)
    address_text = CharField(source='address.address', read_only=True)
    items = CommissionProductSerializer(source='commission_product_set', many=True, read_only=True)

    class Meta:
        model = models.Commission
        fields = [
            'id', 'user', 'user_nickname', 'address', 'address_text',
            'status', 'total', 'items',
        ]