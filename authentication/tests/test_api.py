from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class CreateCustomerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("authentication:create")
        self.valid_payload = {
            "email": "test@example.com",
            "password": "password123",
        }
        self.invalid_payload = {
            "email": "test@example.com",
        }

    def test_create_customer_success(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(
            response.cookies.get(settings.SIMPLE_JWT["AUTH_COOKIE"]).value,
            response.data["refresh"],
        )

    def test_create_customer_invalid(self):
        response = self.client.post(self.url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("authentication:login")
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.valid_payload = {
            "email": "test@example.com",
            "password": "password123",
        }
        self.invalid_payload = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }

    def test_login_success(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn(settings.SIMPLE_JWT["AUTH_COOKIE"], response.cookies)

    def test_login_invalid(self):
        response = self.client.post(self.url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.url = reverse("authentication:token_refresh")
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = str(self.refresh)

    def test_refresh_token_success(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_invalid(self):
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = "invalidtoken"
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ManageUserViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = str(self.refresh)
        self.url = reverse("authentication:profile")

    def test_manage_user_success(self):
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_manage_user_unauthorized(self):
        self.client.cookies.clear()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
