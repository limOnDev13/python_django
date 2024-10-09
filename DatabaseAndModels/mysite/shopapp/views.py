from typing import Dict, Any

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from shopapp.models import Product, Order


# Create your views here.
def shop_index(request: HttpRequest) -> HttpResponse:
    context: Dict[str, Any] = {
        "links": [
            ("/products", "http://localhost:8000/shop/products/"),
            ("/orders", "http://localhost:8000/shop/orders/"),
        ]
    }
    return render(
        request, "shopapp/shop-index.html", context=context
    )


def products_list(request: HttpRequest) -> HttpResponse:
    context: Dict[str, Any] = {
        "products": Product.objects.all()
    }
    return render(request, "shopapp/products-list.html", context=context)


def orders_list(request: HttpRequest) -> HttpResponse:
    context: Dict[str, Any] = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, "shopapp/orders-list.html", context=context)
