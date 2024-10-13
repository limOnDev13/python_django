from django.urls import path

from .views import (shop_index, groups_list,
                    ProductsListView, ProductDetailView, ProductDeleteView,
                    ProductUpdateView, ProductCreateView,
                    OrderListView, OrderDetailView, OrderCreateView)

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/create", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order_details"),
    path("orders/create", OrderCreateView.as_view(), name="order_create"),
]
