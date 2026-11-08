from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, ValidationError

from balenciaga_app import models
from balenciaga_app.models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    nickname = CharField(source='username', max_length=150)
    telephone = CharField(source='profile.telephone', required=False, allow_blank=True, max_length=50)
    password = CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'telephone', 'password']

    def validate_nickname(self, value):
        value = value.strip()
        qs = User.objects.filter(username__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Никнейм уже занят')
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if value and qs.exists():
            raise ValidationError('Email уже используется')
        return value

    def create(self, validated_data):
        telephone = validated_data.pop('profile', {}).get('telephone', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Profile.objects.create(user=user, telephone=telephone)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if 'telephone' in profile_data:
            Profile.objects.update_or_create(user=instance, defaults={'telephone': profile_data['telephone']})
        return instance


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
    user_nickname = CharField(source='user.username', read_only=True)
    address_text = CharField(source='address.address', read_only=True)
    items = CommissionProductSerializer(source='commission_product_set', many=True, read_only=True)

    class Meta:
        model = models.Commission
        fields = [
            'id', 'user', 'user_nickname', 'address', 'address_text',
            'status', 'total', 'items',
        ]