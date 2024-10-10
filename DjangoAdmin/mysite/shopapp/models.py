from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30, null=False, verbose_name="Product name")
    description = models.TextField(blank=True, null=True, verbose_name="Product description")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Price without discount")
    discount = models.PositiveSmallIntegerField(default=0, verbose_name="Current discount")
    archived = models.BooleanField(default=True, null=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "products"


class Order(models.Model):
    description = models.TextField(null=True, verbose_name="Order description")
    address = models.CharField(max_length=200, null=False, verbose_name="User address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date and time of creation order")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="User name")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="List of products in order")

    class Meta:
        ordering = ["-created_at", "user", "pk"]
        verbose_name_plural = "orders"
