from django.urls import path

from . import views


app_name = "contacts"

urlpatterns = [
    path("", views.main, name="main"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path("update_contact/<int:id>", views.update_contact, name="update_contact"),
    path("delete_contact/<int:id>", views.delete_contact, name="delete_contact"),
]
