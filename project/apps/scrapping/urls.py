from django.urls import path
from . import views

app_name = 'scrapping'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.get_news, name='news'),
    path('sport_news/', views.get_sport_news, name='sport_news'),
    path('tech_news/', views.get_tech_news, name='tech_news'),
    path('python_books/', views.get_python_books, name='python_books'),
    path('currency/', views.get_currency, name='currency'),
]