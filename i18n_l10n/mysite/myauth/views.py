from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse

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
    fields = "biography", "agreement_accepted", "avatar"
    template_name = "myauth/profile_update.html"
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserListView(ListView):
    queryset = User.objects.select_related("profile")
    template_name = "myauth/user_list.html"


class UserDetailView(DetailView):
    queryset = User.objects.select_related("profile")
    template_name = "myauth/about-user.html"
    context_object_name = "object"


class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = "avatar",
    template_name = "myauth/avatar_update.html"

    def get_success_url(self):
        return reverse(
            "myauth:about-user",
            kwargs={"pk": self.object.pk},
        )

    def test_func(self):
        return self.request.user.is_staff or self.get_object().pk == self.request.user.pk
