from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import MyLogoutView, main_page, set_cookie_view, get_cookie_view

app_name = "myauth"

urlpatterns = [
    path("", main_page, name="main_page"),
    path(
        "login/", LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        MyLogoutView.as_view(),
        name="logout"
    ),
    path("set_cookie/", set_cookie_view, name="set_cookie"),
    path("get_cookie/", get_cookie_view, name="get_cookie"),
]
