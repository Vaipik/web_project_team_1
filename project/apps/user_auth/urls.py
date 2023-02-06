from django.urls import re_path

from .views import SignInAjaxView, SignUpView, SignOutAjaxView

app_name = "user_auth"

urlpatterns = [
    re_path(r"^sign_in/$", SignInAjaxView.as_view(), name="login"),
    re_path("^sign_up/$", SignUpView.as_view(), name="registration"),
    re_path(r"^sign_out/$", SignOutAjaxView.as_view(), name="logout"),
]
