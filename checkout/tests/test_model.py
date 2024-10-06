from django.test import TestCase
from django.contrib.auth import get_user_model
from checkout.models import Order, OrderItem, OrderStatus
from shop.tests.test_model import ProductFactory, CategoryFactory
from faker import Faker


class OrderModelTests(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.customer = get_user_model().objects.create_user(
            email=self.fake.email(), password=self.fake.password()
        )

        self.category = CategoryFactory()
        self.category.save()

        self.product = ProductFactory(category=self.category)
        self.product.save()

        self.order = Order.objects.create(
            customer=self.customer,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(),
            phone=self.fake.phone_number(),
            shipping_address=self.fake.address(),
            shipping_city=self.fake.city(),
            shipping_postcode=self.fake.postcode(),
            shipping_country=self.fake.country(),
            status=self.fake.random_element(OrderStatus.choices),
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=self.fake.random_int(min=1, max=10),
            price=self.product.price,
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.first_name, self.order.first_name)
        self.assertEqual(self.order.last_name, self.order.last_name)
        self.assertEqual(self.order.email, self.order.email)
        self.assertEqual(self.order.phone, self.order.phone)
        self.assertEqual(self.order.shipping_address, self.order.shipping_address)
        self.assertEqual(self.order.shipping_city, self.order.shipping_city)
        self.assertEqual(self.order.shipping_postcode, self.order.shipping_postcode)
        self.assertEqual(self.order.shipping_country, self.order.shipping_country)
        self.assertEqual(self.order.status, self.order.status)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, self.order_item.quantity)
        self.assertEqual(self.order_item.price, self.product.price)

    def test_order_string_representation(self):
        self.assertEqual(
            str(self.order),
            f"Order {self.order.id} by {self.order.user.email}",
        )

    def test_order_item_string_representation(self):
        self.assertEqual(
            str(self.order_item),
            f"{self.order_item.quantity} of {self.order_item.product.name} in order {self.order.id}",
        )

    def test_order_item_price_calculation(self):
        self.assertEqual(self.order_item.price, self.product.price)
