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

    def __str__(self):
        return self.address

class Category(models.Model):
    category = models.CharField(max_length=150)

    def __str__(self):
        return self.category

class Size(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return self.size

class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField()
    article_number = models.IntegerField()

    def __str__(self):
        return self.name, self.category

class Size_Product():
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Commission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Commission_Product(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

