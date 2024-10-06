from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from shop.models import Product


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Percentage value (1 to 100)",
    )

    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"{self.code} - {self.discount}%"

    class Meta:
        ordering = ["-id"]


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.email}"
        return f"Cart with session {self.session_key}"

    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        if self.coupon:
            total -= (self.coupon.discount / Decimal(100)) * total
        return total

    def get_total_item(self):
        return sum(item.quantity for item in self.items.all())

    def coupon_is_used(self):
        return bool(self.coupon)

    class Meta:
        ordering = ["-id"]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"

    def item_total_price(self):
        return self.product.price * self.quantity
