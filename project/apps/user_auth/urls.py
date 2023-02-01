from django.urls import re_path

from .views import SignInAjax, SignUpView, sign_out

app_name = "user_auth"

urlpatterns = [
    re_path(r"^sign_in/$", SignInAjax.as_view(), name="login"),
    re_path("^sign_up/$", SignUpView.as_view(), name="registration"),
    re_path(r"^sign_out/$", sign_out, name="logout"),
]
