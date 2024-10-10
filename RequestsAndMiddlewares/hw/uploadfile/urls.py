from django.urls import path

from .views import upload_file, throttling

app_name = "shopapp"

urlpatterns = [
    path("", upload_file, name="upload"),
    path("throttling/", throttling, name="throttling"),
]
