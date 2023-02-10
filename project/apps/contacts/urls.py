from django.urls import path

from . import views


app_name = "contacts"

urlpatterns = [
    path("", views.show_contacts, name="contacts"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path("update_contact/<uuid:pk>", views.update_contact, name="update_contact"),
    path("delete_contact/<uuid:pk>", views.delete_contact, name="delete_contact"),
    path("show_contacts_bd/", views.show_contacts_bd, name="show_contacts_bd"),
]
