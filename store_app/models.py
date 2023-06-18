from django.db import models
from shared.product_app.models import Product
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
    date_completed = models.DateTimeField(auto_now_add=True)


class Billing(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=225)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=225)
    amount = models.FloatField(blank=True, null=True)
