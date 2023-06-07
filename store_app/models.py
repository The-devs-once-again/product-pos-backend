from django.db import models
from product_app.models import Product

# Create your models here.
class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=225)
    order_quantity = models.IntegerField()
    order_status = models.CharField(max_length=225)
    order_total = models.FloatField()
    orders = models.ManyToManyField(Product)


class OrderHistory(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(auto_now_add=True)


class Billing(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=225)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=225)
    amount = models.DecimalField(max_digits=10, decimal_places=2)