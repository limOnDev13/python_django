from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


class ProductsListView(ListView):
    queryset = Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "description", "price", "discount", "archived"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )


class ProductCreateView(CreateView):
    model = Product
    template_name_suffix = "_create_form"
    fields = "name", "description", "price", "discount", "archived"
    success_url = reverse_lazy("shopapp:products_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderDetailView(DetailView):
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
