from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


# Create your views here.
class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "myauth/index.html")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Setting cookie...")
    response.set_cookie("some_var", "some_value", max_age=300)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("some_var", "Var not found")
    return HttpResponse(f"Cookie {value=}")
