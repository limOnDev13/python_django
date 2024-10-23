from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    main_page_view,
    RegisterView,
    ProfileUpdateView,
    UserDetailView,
    UserListView,
    AvatarUpdateView,
)


from .views import (
    AboutMeView,
)

app_name = "myauth"

urlpatterns = [
    path("main-page/", main_page_view, name="main_page"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("about-user/<int:pk>", UserDetailView.as_view(), name="about-user"),
    path("user-list/", UserListView.as_view(), name="user-list"),
    path("update-profile/", ProfileUpdateView.as_view(), name="update-profile"),
    path("update-avatar/<int:pk>", AvatarUpdateView.as_view(), name="update-avatar")
]
