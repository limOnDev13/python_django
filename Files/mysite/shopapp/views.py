import re
from typing import List, Dict, Any

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order


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
