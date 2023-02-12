from django.urls import path

from . import views


app_name = "user_profile"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit_profile/", views.EditProfile.as_view(), name="edit_profile")
    # path("edit_profile/", views.edit_profile, name="edit_profile")
]
