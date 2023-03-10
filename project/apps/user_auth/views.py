from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView

from .forms import SignUpForm


class SignInAjaxView(View):

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)  # If user exists
            if user:
                login(request, user)
                return JsonResponse(
                    data={
                        "message": "Logged in",
                        "status": 200,
                        "url": redirect("user_profile:profile").url
                    },
                    status=200
                )

        return JsonResponse(
                data={"message": "Invalid credentials", "status": 400},
                status=200
        )


class SignUpView(CreateView):
    template_name = "user_auth/sign_up.html"
    form_class = SignUpForm
    extra_context = {"title": "Registration page"}

    def get_success_url(self):
        login(self.request, self.object)  # To login created user, self.object -> created user
        """Redirects user to created profile page"""
        return reverse_lazy("user_profile:profile")  #


class SignOutAjaxView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect("user_auth:registration")
