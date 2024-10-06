from rest_framework.test import APITestCase
from rest_framework import status
from email_subscription.models import SubscribedUser
from email_subscription.serializers import EmailSubscriptionSerializer
from faker import Faker


class EmailSubscriptionSerializerTest(APITestCase):

    def setUp(self):
        self.fake = Faker()
        self.valid_email = self.fake.email()
        self.invalid_email = "invalid-email"

    def test_valid_data(self):
        data = {"email": self.valid_email}
        serializer = EmailSubscriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], self.valid_email)

    def test_invalid_email(self):
        data = {"email": self.invalid_email}
        serializer = EmailSubscriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_create_subscription(self):
        data = {"email": self.valid_email}
        serializer = EmailSubscriptionSerializer(data=data)
        if serializer.is_valid():
            subscription = serializer.save()
            self.assertEqual(subscription.email, self.valid_email)
        else:
            self.fail(f"Serializer is not valid. Errors: {serializer.errors}")

    def test_duplicate_email(self):
        SubscribedUser.objects.create(email=self.valid_email)
        data = {"email": self.valid_email}
        serializer = EmailSubscriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
