from django.shortcuts import render

from .services.scrapy_news import scrapy_ukr_news, scrapy_sport_news, scrapy_tech_news, scrapy_python_books, \
    scrapy_currency


# Create your views here.
def index(request):
    return render(request, 'scrapping/index.html')


def get_news(request):
    news = scrapy_ukr_news()
    return render(request, 'scrapping/scrape_news.html', {'news': news})


def get_sport_news(request):
    sport_news = scrapy_sport_news()
    return render(request, 'scrapping/scrape_sport_news.html', {'sport_news': sport_news})


def get_tech_news(request):
    tech_news = scrapy_tech_news()
    return render(request, 'scrapping/scrape_tech_news.html', {'tech_news': tech_news})


def get_python_books(request):
    python_books = scrapy_python_books()
    return render(request, 'scrapping/scrape_python_books.html', {'python_books': python_books})


def get_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        date = request.POST.get('date')
        currency_list = scrapy_currency(currency, date)
        return render(request, 'scrapping/scrape_currency.html',
                      {'currency_list': currency_list, 'currency': currency, 'date': date})
    return render(request, 'scrapping/scrape_currency.html')
