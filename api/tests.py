from datetime import date
from django.test import client
from rest_framework.test import APITestCase, RequestsClient
from django.urls import reverse
from api_auth.models import User
from api.models import Shop
from rest_framework import status


class SupplierTest(APITestCase):
    def test_uplod_file_permision(self):
        data = {
            "email": "user@user.com",
            "password": "password",
        }
        user = User.objects.create_user(**data)
        user.user_type = "shop"
        user.save()
        url = reverse("api-login")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"login": True})

        shop = Shop.objects.create(name="shop", owner=user, delivery_price=20)
        url = reverse("api-shop-update")
        data = open("fixture/shop1.yaml").read()
        response = self.client.post(url, content_type="application/yaml", data=data)
