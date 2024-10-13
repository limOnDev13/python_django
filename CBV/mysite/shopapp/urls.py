from django.urls import path

from .views import (shop_index, groups_list,
                    ProductsListView, orders_list, ProductDetailView,
                    ProductUpdateView, ProductCreateView)

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_details"),
    path("products/update/<int:pk>", ProductUpdateView.as_view(), name="product_update"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("orders/", orders_list, name="orders_list"),
]
