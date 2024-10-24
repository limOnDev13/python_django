from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        verbose_name = _("name of product model")
        verbose_name_plural = _("plural name of product model")
        ordering = ["name", "price"]

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})


class Order(models.Model):
    class Meta:
        verbose_name = _("name of order model")
        verbose_name_plural = _("plural name of order model")

    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
