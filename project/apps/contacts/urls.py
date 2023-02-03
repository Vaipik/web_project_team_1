from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_contact/', views.add_contact, name='add_contact'),
]
