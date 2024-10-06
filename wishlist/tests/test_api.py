from django.db.migrations import serializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from shop.models import Product, Category
from wishlist.services import WishlistService


class WishlistTests(APITestCase):
    def setUp(self):
        self.fake = Faker()

        self.category = Category.objects.create(
            name=self.fake.word(), slug=self.fake.slug()
        )

        self.product = Product.objects.create(
            name=self.fake.word(),
            category=self.category,
            slug=self.fake.slug(),
            price=self.fake.pydecimal(left_digits=5, right_digits=2, positive=True),
            SKU=self.fake.unique.random_number(digits=6),
            description=self.fake.text(),
            views=self.fake.random_number(digits=2),
        )

    def test_get_wishlist(self):
        self.client.post(reverse("add_to_wishlists", args=[self.product.id]))

        url = reverse("wishlists")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertTrue(hasattr(response.data["products"], "__iter__"))
        product_iterator = response.data["products"]
        has_products = any(True for _ in product_iterator)
        self.assertTrue(has_products)

    def test_add_to_wishlist(self):
        url = reverse("add_to_wishlists", args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wishlist_service = WishlistService(self.client)
        products = wishlist_service.wishlist
        self.assertIn(str(self.product.id), products)

    def test_remove_from_wishlist(self):
        url = reverse("remove_from_wishlists", args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse("wishlists")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertFalse(
            any(
                item["product"]["id"] == str(self.product.id)
                for item in response.data["products"]
            )
        )
