from rest_framework import serializers
from .models import Size, AddOn, Variation, Product
from .factories.product_object_factory import ProductFactory

product_factory = ProductFactory()

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('size_choice', 'size_price')


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = ('add_on_choice', 'add_on_price')


class VariationSerializer(serializers.ModelSerializer):
    size = SizeSerializer(many=True, required=False)
    add_on = AddOnSerializer(many=True, required=False)

    class Meta:
        model = Variation
        fields = ('size', 'add_on')


class ProductSerializer(serializers.ModelSerializer):
    variation = VariationSerializer(required=False)

    class Meta:
        model = Product
        fields = ('product_name', 'product_price', 'product_type', 'category', 'variation')

    def create(self, validated_data):
        return product_factory.create_object(validated_data)

    def update(self, instance, validated_data):
        return product_factory.update_object(instance, validated_data)
