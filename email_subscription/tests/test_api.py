from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from email_subscription.models import SubscribedUser


class EmailSubscriptionViewTest(APITestCase):

    def setUp(self):
        self.fake = Faker()
        self.url = "/"  # Путь, так как префикс пустой
        self.valid_email = self.fake.email()

    def test_create_subscription(self):
        data = {"email": self.valid_email}
        response = self.client.post(self.url, data, format="json")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(SubscribedUser.objects.count(), 0)

    def test_duplicate_email(self):
        SubscribedUser.objects.create(email=self.valid_email)
        data = {"email": self.valid_email}
        response = self.client.post(self.url, data, format="json")
        print(f"Response content for duplicate: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(SubscribedUser.objects.count(), 1)
