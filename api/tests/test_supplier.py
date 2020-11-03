from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from unittest.mock import patch
from django.test import override_settings

from api.models import Parameter, Shop, Category, Product, ProductParameter
from api_auth.models import User
from marketplace.marketplace.celery import app
from celery.contrib.testing.worker import start_worker

from . import td


class SupplierTest(APITestCase):
    # allow_database_queries = True

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()

    #     # Start up celery worker
    #     cls.celery_worker = start_worker(app)
    #     cls.celery_worker.__enter__()

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()

    #     # Close worker
    #     cls.celery_worker.__exit__(None, None, None)

    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "email": "user@user.com",
            "password": "password",
        }
        cls.user = User.objects.create_user(**user_data)
        cls.user.user_type = "shop"
        cls.user.save()


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_uplod_file(self):
        self.client.force_login(self.user)
        Shop.objects.create(name='shop', owner=self.user)
        url = reverse("api-shop-update")
        response = self.client.post(
            url, content_type="application/yaml", data=td.base_yaml
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Shop.objects.get())
        self.assertEqual(len(Product.objects.all()), 1)
        

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
