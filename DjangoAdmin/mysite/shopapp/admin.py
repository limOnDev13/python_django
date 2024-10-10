from django.contrib import admin

from .models import Product, Order


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description", "price", "archived"
    search_fields = "pk", "name", "description"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "description", "address", "created_at", "user"
    search_fields = "pk", "description", "user"
