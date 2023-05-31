from django.db import models


class Products(models.Model):
    product_name = models.CharField(max_length=225)
    product_price = models.FloatField()