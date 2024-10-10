from django.urls import path

from .views import upload_file

app_name = "shopapp"

urlpatterns = [
    path("", upload_file, name="index"),
]
