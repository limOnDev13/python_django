from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    ProductDetailsView,
    ProductsListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    export_orders_to_json,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    export_user_orders_csv,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/export/", export_orders_to_json, name="export-orders"),
    path("api/", include(routers.urls)),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user-orders"),
    path("users/<int:user_id>/orders/export/", export_user_orders_csv, name="user-orders-export"),
]
