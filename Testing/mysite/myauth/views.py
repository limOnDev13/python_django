from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from .models import Profile


def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "myauth/main-page.html")


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = "biography", "agreement_accepted"
    template_name = "myauth/profile_update.html"
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        return self.request.user.profile
