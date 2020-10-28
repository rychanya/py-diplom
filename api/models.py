from django.contrib.auth import get_user_model
from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    delivery_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    status = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Parameter(models.Model):
    name = models.CharField(max_length=100)


class BaseProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Product(models.Model):
    base = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=19, decimal_places=2)
    parameters = models.ManyToManyField(Parameter, through="ProductParameter")
    model = models.CharField(max_length=100)


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()
