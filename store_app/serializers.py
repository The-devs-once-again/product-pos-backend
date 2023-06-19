from rest_framework import serializers
from shared.product_app.serializers import ProductSerializer
from store_app.store_factories.store_object_factory import ItemFactory, OrderFactory, BillingFactory
from .models import Item, Order, Billing

order_factory = OrderFactory()
billing_factory = BillingFactory()


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=False)

    class Meta:
        model = Item
        fields = ['uuid', 'amount', 'item_quantity', 'product']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['uuid'] = data.get('uuid')
        return ret

    def create(self, validated_data):
        return ItemFactory().create_object(validated_data=validated_data)
    
    def update(self, instance, validated_data):
        return ItemFactory().update_object(instance, validated_data=validated_data)


class OrderSerializer(serializers.ModelSerializer):
    item_list = ItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ['order_date', 'ref_id', 'order_id', 'order_quantity', 'order_status', 'item_list']

    def create(self, validated_data):
        return order_factory.create_object(validated_data=validated_data)

    def update(self, instance, validated_data):
        order = order_factory.update_object(instance, validated_data=validated_data)
        order_factory.update_billing_amount(order)

        return order


class BillingSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=False)
    
    class Meta:
        model = Billing
        fields = ['date', 'ref_id', 'amount', 'payment_method', 'order']

    def create(self, validated_data):
        return billing_factory.create_object(validated_data=validated_data)
    