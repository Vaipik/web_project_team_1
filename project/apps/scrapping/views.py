from datetime import datetime

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.

URL = ['https://www.pravda.com.ua/news/',
       'https://sport.ua/uk',
       'https://ain.ua/post-list/',
       'https://www.goodreads.com/list/show/32685.Best_Python_programming_books',
       'https://minfin.com.ua/ua/currency/banks/',
       ]


def index(request):
    return render(request, 'scrapping/index.html')


def get_news(request):
    news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(URL[0], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.select('div[class="container_sub_news_list_wrapper mode1"] div[class="article_news_list"]')
    for item in data:
        news_item = {}
        news_item['created'] = item.find('div', class_='article_time').text.strip()
        news_item['title'] = item.find('div', class_='article_header').text.strip()
        link = item.find('a').get('href')
        if 'https://www.epravda.com.ua' in link:
            news_item['link'] = link
        else:
            news_item['link'] = 'https://www.pravda.com.ua' + link
        news.append(news_item)
        # print(news_item)
    return render(request, 'scrapping/scrape_news.html', {'news': news})


def get_sport_news(request):
    sport_news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(URL[1], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find('div', class_='news-items').find_all('div', class_='item')
    for item in data:
        news_item = {}
        news_item['created'] = item.find('span', class_='item-date').text.strip()
        news_item['title'] = item.find('div', {'class': 'item-title'}).text.strip()
        news_item['category'] = item.find('span', class_='item-sport').text.title()
        news_item['link'] = item.find('a').get('href')
        sport_news.append(news_item)
        # print(news_item) # for debug
    return render(request, 'scrapping/scrape_sport_news.html', {'sport_news': sport_news})


def get_tech_news(request):
    tech_news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(URL[2], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('li', class_='post-item ordinary-post')
    for el in data:
        news_item = {}
        news_item['created'] = el.find('div', class_='post-date').text.strip()
        news_item['title'] = el.find('a').text.strip()
        news_item['link'] = el.find('a').get('href')
        tech_news.append(news_item)
    data_2 = soup.find_all('div', class_='big-post-preview')
    for el in data_2:
        news_item = {}
        news_item['created'] = el.find('div', class_='post-date web-view').text.strip()
        news_item['title'] = el.find('a').text.strip()
        news_item['link'] = el.find('a').get('href')
        tech_news.append(news_item)
    return render(request, 'scrapping/scrape_tech_news.html', {'tech_news': tech_news})


def get_python_books(request):
    python_books = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(URL[3], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.select('table[class="tableList js-dataTooltip"] tr[itemtype="http://schema.org/Book"]')
    for el in data:
        book_item = {}
        book_item['title'] = el.find('a', class_='bookTitle').text.strip()
        book_item['author'] = el.find('span', itemtype='http://schema.org/Person').text.strip()
        book_item['rating'] = el.find('span', class_='minirating').text.strip()
        rel_link = el.find('a', class_='bookTitle').get('href')
        book_item['link'] = 'https://www.goodreads.com' + rel_link
        book_item['image'] = el.find('img').get('src')
        python_books.append(book_item)
    return render(request, 'scrapping/scrape_python_books.html', {'python_books': python_books})


def get_currency(request):
    currency_list = []
    if request.method == 'POST':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/89.0.4389.114 Safari/537.36'}
        currency = request.POST['currency']
        date = request.POST.get('date')
        try:
            act_date = datetime.strptime(str(date), '%Y-%m-%d').date()
        except ValueError:
            act_date = datetime.now().date()
        full_url = f"{URL[4]}{currency.lower()}/{act_date}/"
        response = requests.get(full_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find('tbody', class_='list').find_all('tr')
        for el in data:
            currency_item = {}
            currency_item['bank'] = el.find('a', {'class': 'mfm-black-link'}).text.strip()
            sub_link = el.find('a', {'class': 'mfm-black-link'}).get('href')
            currency_item['link'] = 'https://minfin.com.ua' + sub_link
            currency_item['buy'] = el.find('td', class_='responsive-hide mfm-text-right mfm-pr0').text.strip()
            if len(currency_item['buy']) == 0:
                currency_item['buy'] = '0.0000'
            currency_item['sell'] = el.find('td', class_='responsive-hide mfm-text-left mfm-pl0').text.strip()
            if len(currency_item['sell']) == 0:
                currency_item['sell'] = '0.0000'
            currency_item['update'] = el.find('td', class_='respons-collapsed mfcur-table-refreshtime').text.strip()
            currency_list.append(currency_item)
        context = {'currency_list': currency_list, 'currency': currency, 'date': act_date}
        return render(request, 'scrapping/scrape_currency.html', context)
    return render(request, 'scrapping/scrape_currency.html')
