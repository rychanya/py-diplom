from django.http import request
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Parameter, Shop, Category, Product, ProductParameter
from api_auth.models import User

from . import td


class SupplierTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "email": "user@user.com",
            "password": "password",
        }
        cls.user = User.objects.create_user(**user_data)
        cls.user.user_type = "shop"
        cls.user.save()

    def test_uplod_file(self):
        self.client.force_login(self.user)
        url = reverse("api-shop-update")
        response = self.client.post(
            url, content_type="application/yaml", data=td.base_yaml
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "ok")
        category = Category.objects.get()
        self.assertEqual(category.name, td.category1["name"])
        product = Product.objects.get()
        for key, value in td.goods1.items():
            if key == "category":
                self.assertEqual(product.base.category.id, value)
            elif key == "name":
                self.assertEqual(product.base.name, value)
            elif key == "parameters":
                continue
            else:
                self.assertEqual(getattr(product, key), value)
        for parameter in ProductParameter.objects.get_queryset().all():
            self.assertEqual(
                parameter.value, td.goods1["parameters"][parameter.parameter.name]
            )
            self.assertEqual(parameter.product, product)

    def test_uplod_file_by_not_owner(self):
        other_user = User.objects.create_user(
            email="other@user.com", password="password"
        )
        Shop.objects.create(name="not owner", owner=other_user)
        self.client.force_login(self.user)
        url = reverse("api-shop-update")
        response = self.client.post(
            url, content_type="application/yaml", data=td.not_shop_owner_yaml
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_shop_settings(self):
        self.client.force_login(self.user)
        url = reverse("shop-settings")
        shop_name = "shop"
        shop = Shop.objects.create(name=shop_name, owner=self.user, delivery_price=20)
        data = {
            "status": False,
            "name": shop_name,
            "delivery_price": 0,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shop.refresh_from_db()
        self.assertEqual(shop.status, False)
        self.assertEqual(shop.delivery_price, 0)
