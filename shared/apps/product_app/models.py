from django.db import models


class Size(models.Model):
    size_choice = models.CharField(max_length=225)
    size_price = models.FloatField()


class AddOn(models.Model):
    add_on_choice = models.CharField(max_length=225)
    add_on_price = models.FloatField()


class Variation(models.Model):
    size = models.ManyToManyField(Size)
    add_on = models.ManyToManyField(AddOn)


class Product(models.Model):
    product_name = models.CharField(max_length=225)
    product_price = models.FloatField()
    product_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    variation = models.OneToOneField(Variation, on_delete=models.CASCADE, null=True, blank=True)