"""This file is responsible for making store object factories"""

from typing import Any
from django.db import models

from shared.factories.object_factory import ObjectFactory
from shared.product_app.factories.product_object_factory import ProductFactory
from store_app.models import Order, Item
from django.utils.crypto import get_random_string


class ItemFactory(ObjectFactory):
    """Concrete store object factory creates an item object. This factory implements the 
        abstract ObjectFactory"""

    @staticmethod
    def _check_variation_size(size_list: list) -> bool:
        """Checks if the size list is empty or not"""

        size_exists: bool = False

        if size_list:
            size_exists = True
        else:
            return size_exists

        return size_exists

    @staticmethod
    def _get_variation_total_amount(size_list, add_on_list) -> tuple[int, int]:
        """Gets the total amount of the size and add on list. It first checks if it
        is a dictionary or an instance
        """

        size_price_total = 0
        add_on_price_total = 0

        if isinstance(size_list, models.Manager):
            size_list = size_list.all()
        for size_price in size_list:
            if isinstance(size_price, dict):
                size_price_total += size_price['size_price']
            else:
                size_price_total += size_price.size_price

        if isinstance(add_on_list, models.Manager):
            add_on_list = add_on_list.all()
        for add_on_price in add_on_list:
            if isinstance(add_on_price, dict):
                add_on_price_total += add_on_price['add_on_price']
            else:
                add_on_price_total += add_on_price.add_on_price

        return size_price_total, add_on_price_total

    def _get_item_total(self, product_data, item_quantity: int) -> float:
        """"Gets the item total by adding the vartion field prices"""

        if isinstance(product_data, dict):
            product_price = product_data['product_price']
            product_variation = product_data.get('variation', None)
        else:
            product_price = product_data.product_price
            product_variation = product_data.variation

        if product_variation:
            if isinstance(product_variation, dict):
                variation_copy = dict(product_variation)
            else:
                variation_copy = {
                    'size': product_variation.size,
                    'add_on': product_variation.add_on
                }

            size_list = variation_copy.get('size', [])
            add_on_list = variation_copy.get('add_on', [])

            variation_size = self._check_variation_size(size_list)
            size_price_total, add_price_total = self._get_variation_total_amount(size_list, add_on_list)

            if variation_size and add_on_list:
                item_total = size_price_total + add_price_total
            elif variation_size:
                item_total = size_price_total
            else:
                item_total = product_price + add_price_total

            return item_total * item_quantity
        else:
            return product_price * item_quantity

    def create_object(self, validated_data) -> models.Model:
        """"Creates the item object the returns an item instance"""

        product_data = validated_data.pop('product')
        item_quantity = validated_data['item_quantity']
        item_amount = self._get_item_total(product_data, item_quantity)

        product = ProductFactory().create_object(product_data)

        item = Item.objects.create(amount=item_amount, item_quantity=item_quantity, product=product)

        return item

    def update_object(self, instance, validated_data) -> Any:
        # Update the item fields
        item_quantity = validated_data['item_quantity']
        instance.item_quantity = item_quantity

        # Update product
        product_data = validated_data.get('product')
        if product_data:
            product = instance.product
            ProductFactory().update_object(product, product_data)

            instance.amount = self._get_item_total(product, item_quantity)

        instance.save()

        return instance


class OrderFactory(ObjectFactory):
    """Concrete store object factory creates an order object. This factory implements 
        the abstract ObjectFactory"""

    def create_object(self, validated_data) -> models.Model:
        item_list_data = validated_data.pop('item_list', [])

        item_list = []
        for item_data in item_list_data:
            item = ItemFactory().create_object(item_data)
            item_list.append(item)

        order_id = get_random_string(length=6).upper()
        order_quantity = len(item_list)

        order = Order.objects.create(order_id=order_id, order_quantity=order_quantity, order_status="ONGOING")
        order.item_list.set(item_list)

        return order

    def update_object(self, instance, validated_data) -> Any:
        # Update order fields
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.order_id = validated_data.get('order_id', instance.order_id)
        instance.order_quantity = validated_data.get('order_quantity', instance.order_quantity)
        instance.order_status = validated_data.get('order_status', instance.order_status)

        # Update items
        item_list = validated_data.get('item_list')
        if item_list:
            for item_data in item_list:
                product_code = item_data['product']['product_code']
                item = Item.objects.filter(product__product_code=product_code).first()
                if item:
                    ItemFactory().update_object(item, item_data)

        instance.save()

        return instance
