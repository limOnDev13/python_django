from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse


def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "myauth/main-page.html")


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"
