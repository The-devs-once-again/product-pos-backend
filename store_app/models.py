from django.db import models
from shared.apps.product_app.models import Product
from django.utils.crypto import get_random_string
import uuid

# Create your models here.


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False) 
    amount = models.FloatField(default=0, blank=True, null=True)
    item_quantity = models.IntegerField(default=0, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    ref_id = models.CharField(max_length=225, blank=True, null=True)
    order_id = models.CharField(max_length=225, blank=True, null=True)
    order_quantity = models.IntegerField(default=0, blank=True, null=True)
    order_status = models.CharField(max_length=225)
    item_list = models.ManyToManyField(Item)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = get_random_string(length=6).upper()
        super().save(*args, **kwargs)


class OrderHistory(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=225, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=225)
    amount = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.ref_id:
            self.ref_id = get_random_string(length=12).upper()
            self.order.ref_id = self.ref_id
            self.order.save()

        super().save(*args, **kwargs)
