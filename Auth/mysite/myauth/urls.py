from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import MyLogoutView, main_page

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
]
