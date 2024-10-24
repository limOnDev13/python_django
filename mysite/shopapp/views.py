import re
from typing import List, Dict, Any
import csv

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core import serializers
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(LoginRequiredMixin, DetailView):
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"


class ProductsListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False).select_related("created_by")


class ProductCreateView(PermissionRequiredMixin, CreateView):
    # permissions
    permission_required = "shopapp.add_product",

    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        match = re.search(r"/(\d+)/update/$", self.request.path)
        product_id: int = int(match.group(1))
        return (self.request.user.has_perm("shopapp.change_product")
                and Product.objects.filter(id=product_id).first())


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(LoginRequiredMixin, DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


@user_passes_test(lambda user: user.is_staff)
def export_orders_to_json(request: HttpRequest) -> JsonResponse:
    orders: List[Order] = Order.objects.all()
    result_json: Dict[str, Any] = {
        "orders": [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.id,
                "products_ids": [
                    product.pk
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
    }
    return JsonResponse(result_json)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("created_by").all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter, OrderingFilter
    ]
    search_fields = (
        "name",
        "description",
    )
    ordering_fields = [
        "price",
        "discount",
        "name",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("products").all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend, OrderingFilter,
    ]
    search_fields = (
        "delivery_address",
        "user"
    )
    ordering_fields = [
        "created_at",
        "user",
    ]


class LatestProductsFeed(Feed):
    title = "List of products (latest)"
    description = "Updates on changes and addition list products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.order_by("-created_at")[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/user-orders.html"

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])

        return (Order.objects.filter(user=self.owner)
                .prefetch_related("products"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        # В задании написано, что нужно изменить контекст,
        # но не написано, что именно нужно изменить
        context["owner"] = {
            "username": self.owner.username,
            "pk": self.owner.pk,
        }
        return context


def export_user_orders_csv(request: HttpRequest, user_id: int) -> HttpResponse:
    cache_key: str = f"{user_id}_user_orders"
    data = cache.get(cache_key)

    if not data:
        print("Cache is empty!")
        owner: User = get_object_or_404(User, pk=user_id)
        orders: List[Order] = Order.objects.filter(user=owner).all()
        data = serializers.serialize('json', orders)
        cache.set(cache_key, data, 300)

    return HttpResponse(data, content_type='application/json')
