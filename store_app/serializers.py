from rest_framework import serializers
from .models import Order, OrderHistory, Billing
from product_app.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    orders = ProductSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ['order_date', 'order_id', 'order_quantity', 'order_status', 'order_total', 'orders']


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['orders', 'date_created', 'date_completed']


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ['orders', 'ref_id', 'date_created', 'date_completed', 'payment_method', 'amount']
