from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart, CartItem, Coupon
from shop.models import Category, Product
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("word")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("word")
    category = SubFactory(CategoryFactory)
    slug = Faker("slug")
    price = Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    SKU = Faker("random_number", digits=10)
    description = Faker("text")


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = Faker("word")
    discount = Faker("random_int", min=1, max=100)
    active = True
    valid_from = timezone.now()
    valid_to = timezone.now() + timedelta(days=30)


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = Faker("email")
    password = Faker("password")


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = SubFactory(CustomerFactory)
    coupon = SubFactory(CouponFactory)


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = SubFactory(CartFactory)
    product = SubFactory(ProductFactory)
    quantity = Faker("random_int", min=1, max=10)


class CartModelTest(TestCase):
    def setUp(self):
        self.cart = CartFactory()
        self.cart_item1 = CartItemFactory(cart=self.cart)
        self.cart_item2 = CartItemFactory(cart=self.cart)

    def test_get_total_price(self):
        total_without_coupon = (
            Decimal(self.cart_item1.product.price) * self.cart_item1.quantity
            + Decimal(self.cart_item2.product.price) * self.cart_item2.quantity
        )

        if self.cart.coupon and self.cart.coupon.active:
            expected_total = total_without_coupon - (
                (Decimal(self.cart.coupon.discount) / Decimal(100))
                * total_without_coupon
            )
        else:
            expected_total = total_without_coupon
        self.assertEqual(self.cart.get_total_price(), expected_total)

    def test_get_total_item(self):
        self.assertEqual(
            self.cart.get_total_item(),
            self.cart_item1.quantity + self.cart_item2.quantity,
        )

    def test_coupon_is_used(self):
        self.assertTrue(self.cart.coupon_is_used())


class CartItemModelTest(TestCase):
    def setUp(self):
        self.cart_item = CartItemFactory()

    def test_item_total_price(self):
        self.assertEqual(
            self.cart_item.item_total_price(),
            Decimal(self.cart_item.product.price) * self.cart_item.quantity,
        )


class CouponModelTest(TestCase):
    def setUp(self):
        self.coupon = CouponFactory()
        self.expired_coupon = CouponFactory(
            valid_from=timezone.now() - timedelta(days=30),
            valid_to=timezone.now() - timedelta(days=1),
        )
        self.inactive_coupon = CouponFactory(active=False)

    def test_valid_coupon(self):
        now = timezone.now()
        self.assertTrue(self.coupon.active)
        self.assertLessEqual(self.coupon.valid_from, now)
        self.assertGreaterEqual(self.coupon.valid_to, now)

    def test_inactive_coupon(self):
        self.assertFalse(self.inactive_coupon.active)

    def test_expired_coupon(self):
        now = timezone.now()
        self.assertLess(self.expired_coupon.valid_to, now)
