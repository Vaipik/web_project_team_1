from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from utils.pagination import get_paginator
from .services.scrapy_news import scrapy_ukr_news, scrapy_sport_news, scrapy_tech_news, scrapy_python_books, \
    scrapy_currency


# Create your views here.
# @login_required
def index(request):
    return render(request, 'scrapping/index.html')


# @login_required
def get_news(request):
    news = scrapy_ukr_news()
    page_obj, pages = get_paginator(request, news, 10)
    return render(request, 'scrapping/scrape_news.html', {'page_obj': page_obj, 'pages': pages})


@login_required
def get_sport_news(request):
    sport_news = scrapy_sport_news()
    page_obj, pages = get_paginator(request, sport_news, 10)
    return render(request, 'scrapping/scrape_sport_news.html', {'page_obj': page_obj, 'pages': pages})


@login_required
def get_tech_news(request):
    tech_news = scrapy_tech_news()
    page_obj, pages = get_paginator(request, tech_news, 10)
    return render(request, 'scrapping/scrape_tech_news.html', {'page_obj': page_obj, 'pages': pages})


@login_required
def get_python_books(request):
    python_books = scrapy_python_books()
    page_obj, pages = get_paginator(request, python_books, 8)
    return render(request, 'scrapping/scrape_python_books.html', {'page_obj': page_obj, 'pages': pages})


@login_required
def get_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        date = request.POST.get('date')
        currency_list = scrapy_currency(currency, date)
        return render(request, 'scrapping/scrape_currency.html', {'currency_list': currency_list})
    return render(request, 'scrapping/scrape_currency.html')
