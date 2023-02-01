from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import SignUpForm


class SignInAjax(View):

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(request.POST.get("csrftoken"))
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(
                    data={"message": "Logged in", "status": 200},
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
        return reverse_lazy("index")


@login_required
def sign_out(request):
    logout(request)
    return redirect("index")

