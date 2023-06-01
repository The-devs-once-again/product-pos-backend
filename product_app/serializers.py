from rest_framework import serializers
from .models import Price, Size, AddOn, Variation, Product


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price',)


class SizeSerializer(serializers.ModelSerializer):
    size_price = PriceSerializer()

    class Meta:
        model = Size
        fields = ('size_choice', 'size_price')


class AddOnSerializer(serializers.ModelSerializer):
    add_on_price = PriceSerializer()

    class Meta:
        model = AddOn
        fields = ('add_on_choice', 'add_on_price')


class VariationSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    add_on = AddOnSerializer()

    class Meta:
        model = Variation
        fields = ('size', 'add_on')


class ProductSerializer(serializers.ModelSerializer):
    product_price = PriceSerializer()
    variation = VariationSerializer()

    class Meta:
        model = Product
        fields = ('product_name', 'product_price', 'category', 'variation')
