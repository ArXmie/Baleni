from django.db import models

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.nickname

class Address(models.Model):
    address = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.address

class Category(models.Model):
    category = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category

class Size(models.Model):
    size = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        size_self = '{0.size}'
        return size_self.format(self)

class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField()
    article_number = models.IntegerField()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        product_name = '{0.name} | {0.category}'
        return product_name.format(self)
        
class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField()

    class Meta:
        verbose_name = "Товар-Картина"
        verbose_name_plural = "Товары-Картины"

    def __str__(self):
        sp_name = '{0.product.name} | {0.image}'
        return sp_name.format(self)

class Size_Product(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Размер-Товар"
        verbose_name_plural = "Размеры-Товары"

    def __str__(self):
        sp_name = '{0.size.size} - {0.product.name}'
        return sp_name.format(self)

class Commission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    total = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Commission_Product(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Заказ-Товар"
        verbose_name_plural = "Заказы-Товары"

