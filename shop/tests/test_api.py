from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import factory
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Category, Product
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
)
from django.urls import reverse
from shop.tests.test_model import CategoryFactory, ProductFactory


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.category_url = reverse("category-list")

    def test_list_categories(self):
        response = self.client.get(self.category_url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_category(self):
        url = reverse("category-detail", args=[self.category.id])
        response = self.client.get(url)
        serializer = CategorySerializer(self.category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory(name="Test Category")
        self.product1 = ProductFactory(name="Test Product 1", category=self.category)
        self.product2 = ProductFactory(name="Test Product 2", category=self.category)
        self.product_list_url = reverse("product-list")
        self.product_detail_url = lambda pk: reverse("product-detail", args=[pk])

    def test_list_products(self):
        response = self.client.get(self.product_list_url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_products_by_name(self):
        response = self.client.get(self.product_list_url, {"name": self.product1.name})
        products = Product.objects.filter(name__icontains=self.product1.name)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_products_by_price(self):
        response = self.client.get(self.product_list_url, {"ordering": "price"})
        products = Product.objects.order_by("price")
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_products_by_views(self):
        response = self.client.get(self.product_list_url, {"ordering": "views"})
        products = Product.objects.order_by("views")
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_popular_products(self):
        url = reverse("product-popular")
        response = self.client.get(url)
        products = Product.objects.order_by("-views")[:30]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_latest_arrival_products(self):
        url = reverse("product-latest-arrival")
        response = self.client.get(url)
        products = Product.objects.order_by("-pk")[:30]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
