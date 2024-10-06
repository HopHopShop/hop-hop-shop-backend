from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock


class CheckoutTests(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.checkout_url = reverse("checkout")

        self.order_data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "shipping_address": self.fake.address(),
            "shipping_city": self.fake.city(),
            "shipping_postcode": self.fake.postcode(),
            "shipping_country": self.fake.country(),
            "products": [1],
        }

    @patch("checkout.services.OrderService.create_order")
    @patch("checkout.services.PaymentService.stripe_card_payment")
    def test_checkout(self, mock_payment, mock_create_order):
        mock_order = MagicMock(paid=False, status="Pending")
        mock_create_order.return_value = mock_order

        # если все ок
        mock_payment.return_value.status_code = status.HTTP_200_OK
        response = self.client.post(self.checkout_url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "card_information: This field is required."
        )

        # если ошибка при платеже
        mock_payment.return_value.status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.checkout_url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "card_information: This field is required."
        )
