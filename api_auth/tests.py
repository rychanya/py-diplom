from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate

from api_auth.models import User


class AuthTests(APITestCase):
    def test_login_correct_data(self):
        data = {
            "email": "user@user.com",
            "password": "password",
        }
        User.objects.create_user(**data)
        url = reverse("api-login")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"login": True})

    def test_login_incorrect_data(self):
        data = {
            "email": "user@user.com",
            "password": "password",
        }
        url = reverse("api-login")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"login": False})

    def test_logout(self):
        url = reverse("api-logout")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"login": False})

    def test_registration_and_confirm(self):
        url = reverse("api-registration")
        data = {
            "last_name": "last",
            "first_name": "first",
            "middle_name": "middle",
            "email": "email@email.com",
            "password": "password",
            "company": "comp",
            "position": "seo",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get()
        for atr, value in data.items():
            if atr == "password":
                continue
            self.assertEqual(getattr(user, atr), value)
        self.assertEqual(user.is_active, False)
        self.assertEqual(len(mail.outbox), 1)
        confirm_url = mail.outbox[0].body.strip()
        response = self.client.get(confirm_url, format="json")
        user = User.objects.get()
        self.assertEqual(user.is_active, True)

    def test_reset_password(self):
        email = "user@user.com"
        new_password = "new_password"
        User.objects.create(email=email, password="password")
        url = reverse("password_reset")
        response = self.client.post(url, data={"email": email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        reset_url = mail.outbox[0].body.strip()
        response = self.client.post(
            reset_url, data={"password1": new_password, "password2": new_password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = authenticate(email=email, password=new_password)
        self.assertIsNotNone(user)
