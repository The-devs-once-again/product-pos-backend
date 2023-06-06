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
    size = SizeSerializer(many=True, required=False)
    add_on = AddOnSerializer(many=True, required=False)

    class Meta:
        model = Variation
        fields = ('size', 'add_on')


class ProductSerializer(serializers.ModelSerializer):
    product_price = PriceSerializer()
    variation = VariationSerializer(required=False)

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_price', 'product_type', 'category', 'variation')

    def create(self, validated_data):
        variation_data = validated_data.pop('variation', None)

        if variation_data:
            size_data_list = variation_data.pop('size', [])
            add_on_data_list = variation_data.pop('add_on', [])

            size_list = []
            for size_data in size_data_list:
                size_price = Price.objects.create(price=size_data.pop('size_price')['price'])
                size_list.append(Size.objects.create(size_price=size_price, **size_data))

            add_on_list = []
            for add_on_data in add_on_data_list:
                add_on_price = Price.objects.create(price=add_on_data.pop('add_on_price')['price'])
                add_on_list.append(AddOn.objects.create(add_on_price=add_on_price, **add_on_data))

            variation = Variation.objects.create()
            if size_list:
                variation.size.set(size_list)
            if add_on_list:
                variation.add_on.set(add_on_list)
        else:
            variation = None

        product_price = Price.objects.create(price=validated_data.pop('product_price')['price'])
        product = Product.objects.create(product_price=product_price, variation=variation, **validated_data)

        return product

    def update(self, instance, validated_data):
        # Handle updating writable nested fields here
        def validate_product_data(data, data_field):
            if data is not None:
                data_instance = data_field
                for attr, value in data.items():
                    setattr(data_instance, attr, value)
                data_instance.save()

        product_price_data = validated_data.pop('product_price', None)
        validate_product_data(product_price_data, instance.product_price)

        variation_data = validated_data.pop('variation', None)
        validate_product_data(variation_data, instance.variation)

        # Update non-nested fields as usual
        return super().update(instance, validated_data)