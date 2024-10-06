import datetime

from rest_framework import serializers
from cart.models import Cart, CartItem, Coupon
from shop.models import Product
from shop.serializers import ProductSerializer, ProductImageSerializer


class ProductItemSerializer(ProductSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "category", "slug", "price", "images"]

    def get_images(self, obj) -> ProductImageSerializer:
        first_image = obj.product_images.first()
        return ProductImageSerializer(first_image).data if first_image else None


class CartItemSerializer(serializers.ModelSerializer):
    item_total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "added_at", "item_total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price", "item_count"]


class UseCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["code"]


class DateTimeToDateField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, datetime.datetime):
            return value.date()
        return value

    def to_internal_value(self, data):
        try:
            return datetime.datetime.strptime(data, '%d-%m-%Y').date()
        except ValueError:
            raise serializers.ValidationError("Неправильний формат дати. Очікується формат 'DD-MM-YYYY'.")


class CouponSerializer(serializers.ModelSerializer):
    valid_to = DateTimeToDateField()
    valid_from = DateTimeToDateField(read_only=True)

    def create(self, validated_data):
        validated_data['valid_from'] = datetime.date.today()
        return super().create(validated_data)

    class Meta:
        model = Coupon
        fields = "__all__"

