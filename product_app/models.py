from django.db import models


class Price(models.Model):
    price = models.FloatField()


class Size(models.Model):
    size_choice = models.CharField(max_length=225)
    size_price = models.OneToOneField(Price, on_delete=models.CASCADE)


class AddOn(models.Model):
    add_on_choice = models.CharField(max_length=225)
    add_on_price = models.OneToOneField(Price, on_delete=models.CASCADE)


class Variation(models.Model):
    size = models.ManyToManyField(Size)
    add_on = models.ManyToManyField(AddOn)


class Product(models.Model):
    product_name = models.CharField(max_length=225)
    product_price = models.OneToOneField(Price, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    variation = models.OneToOneField(Variation, on_delete=models.CASCADE, null=True, blank=True)
