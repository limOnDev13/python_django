from django.contrib import admin

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description", "price", "archived"
    search_fields = "pk", "name", "description"
    inlines = [
        OrderInline,
    ]
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
            "description": "Section with base info",
        }),
        ("Price", {
            "fields": ("price", "discount"),
            "description": "Section with info about price",
        }),
        ("Extra", {
            "fields": ("archived", ),
            "classes": ("collapse", ),
            "description": "Extra options",
        })
    ]

    def get_queryset(self, request):
        return Product.objects.prefetch_related("orders")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "description", "address", "created_at", "user"
    search_fields = "pk", "description", "user"
