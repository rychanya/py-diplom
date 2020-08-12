from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # url
    # filename

class Category(models.Model):
    shops = models.ManyToManyField(Shop)
    name = models.CharField(max_length=100, unique=True)

class Product(models.Model):
# category
    name = models.CharField(max_length=100, unique=True)

class ProductInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
# name
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
# price_rrc

# class Parameter(models.Model):
# name

# class ProductParameter(models.Model):
# product_info
# parameter
# value

# class Order(models.Model):
# user
# dt
# status

# class OrderItem(models.Model):
# order
# product
# shop
# quantity

# class Contact(models.Model):
# type
# user
# value