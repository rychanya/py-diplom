from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

USER_TYPE_CHOECES = (("shop", "магазин"), ("buyer", "покупатель"))


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user_email = self.normalize_email(email)
        user = self.model(email=user_email, username=user_email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password,)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    middle_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    user_type = models.CharField(
        choices=USER_TYPE_CHOECES, max_length=5, default="buyer"
    )


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_price = models.DecimalField(max_digits=19, decimal_places=2)


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# dt
# status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()


# order
# product
# shop
# quantity

# class Contact(models.Model):
# type
# user
# value
