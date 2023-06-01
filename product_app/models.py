from django.db import models


class Price(models.Model):
    price = models.FloatField()


class Size(models.Model):
    size_choice = models.CharField(max_length=225, default="regular")
    size_price = models.OneToOneField(Price, on_delete=models.CASCADE)


class AddOn(models.Model):
    add_on_choice = models.CharField(max_length=225, default=" ")
    add_on_price = models.OneToOneField(Price, on_delete=models.CASCADE)


class Variation(models.Model):
    size = models.OneToOneField(Size, on_delete=models.CASCADE)
    add_on = models.OneToOneField(AddOn, on_delete=models.CASCADE)


class Product(models.Model):
    product_name = models.CharField(max_length=225)
    product_price = models.OneToOneField(Price, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default=" ")
    variation = models.OneToOneField(Variation, on_delete=models.CASCADE)