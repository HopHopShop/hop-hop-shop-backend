from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from shop.models import Product, Category
from authentication.models import Customer
from faker import Faker
from django.test import TestCase


class CartAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake = Faker()

        self.category = Category.objects.create(
            name=self.fake.word(), slug=self.fake.slug()
        )

        self.product = Product.objects.create(
            name=self.fake.word(),
            category=self.category,
            slug=self.fake.slug(),
            price=self.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            SKU=self.fake.random_number(digits=10),
            description=self.fake.sentence(),
            views=self.fake.random_number(digits=2),
        )

        self.user = Customer.objects.create_user(
            email="test@example.com", password="password"
        )
        self.client.force_authenticate(user=self.user)

    def test_cart_add_item_view(self):
        add_url = reverse("cart:cart_add", kwargs={"product_id": self.product.id})
        response = self.client.post(add_url, {"quantity": 1, "update_quantity": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertIn("total_items", response.data)
        self.assertIn("subtotal_price", response.data)
        self.assertIn("total_price", response.data)
        self.assertIn("coupon_is_used", response.data)

    def test_cart_remove_item_view(self):
        add_url = reverse("cart:cart_add", kwargs={"product_id": self.product.id})
        remove_url = reverse("cart:cart_remove", kwargs={"product_id": self.product.id})
        self.client.post(add_url, {"quantity": 1, "update_quantity": False})
        response = self.client.delete(remove_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_subtract_item_view(self):
        add_url = reverse("cart:cart_add", kwargs={"product_id": self.product.id})
        subtract_url = reverse(
            "cart:cart_subtract", kwargs={"product_id": self.product.id}
        )
        self.client.post(add_url, {"quantity": 5, "update_quantity": True})
        response = self.client.post(subtract_url, {"quantity": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertIn("total_items", response.data)
        self.assertIn("subtotal_price", response.data)
        self.assertIn("total_price", response.data)
        self.assertIn("coupon_is_used", response.data)

    def test_remove_coupon_view(self):
        remove_coupon_url = reverse("cart:coupon_remove")
        response = self.client.post(remove_coupon_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_apply_coupon_view(self):
        apply_coupon_url = reverse("cart:coupon")
        response = self.client.post(apply_coupon_url, {"code": "TESTCOUPON"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
