from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


# Create your views here.
class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "myauth/index.html")
