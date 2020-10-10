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
