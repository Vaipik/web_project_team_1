from datetime import datetime

from bs4 import BeautifulSoup, ResultSet
import requests

from ..libs.scrapy_urls import URL

from ..libs.scrapy_headers import headers


def find_ukr_news_data() -> list:
    """
    Function returns soup object with ukrainian news
    :return: soup object
    """
    response = requests.get(URL['ukrainian_news'], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    ukr_news_data = soup.select('div[class="container_sub_news_list_wrapper mode1"] div[class="article_news_list"]')
    return ukr_news_data


def scrapy_ukr_news(ukr_news_data=None) -> list:
    """
    Function returns list of dictionaries with ukrainian news
    :param ukr_news_data: soup object
    :return: list of dictionaries
    """
    if not ukr_news_data:
        ukr_news_data = find_ukr_news_data()
    news = []
    for item in ukr_news_data:
        news_item = {'created': item.find('div', class_='article_time').text.strip(),
                     'title': item.find('div', class_='article_header').text.strip()}
        link = item.find('a').get('href')
        if 'https://www.epravda.com.ua' in link:
            news_item['link'] = link
        else:
            news_item['link'] = 'https://www.pravda.com.ua' + link
        news.append(news_item)
    return news


def find_sport_news_data() -> list:
    """
    Function returns soup object with sport news
    :return: soup object
    """
    response = requests.get(URL['sport_news'], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sport_news_data = soup.find('div', class_='news-items').find_all('div', class_='item')
    return sport_news_data


def scrapy_sport_news(sport_news_data=None) -> list:
    """
    Function returns list of dictionaries with sport news
    :param sport_news_data: soup object
    :return: list of dictionaries
    """
    if not sport_news_data:
        sport_news_data = find_sport_news_data()
    sport_news = []
    for item in sport_news_data:
        news_item = {'created': item.find('span', class_='item-date').text.strip(),
                     'title': item.find('div', {'class': 'item-title'}).text.strip(),
                     'category': item.find('span', class_='item-sport').text.title(),
                     'link': item.find('a').get('href')}
        sport_news.append(news_item)
    return sport_news


def find_tech_news_data() -> tuple[ResultSet, ResultSet]:
    """
    Function returns soup object with tech news
    :return: soup object
    """
    response = requests.get(URL['tech_news'], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    post_data = soup.find_all('li', class_='post-item ordinary-post')
    big_post_data = soup.find_all('div', class_='big-post-preview')
    return post_data, big_post_data


def scrapy_tech_news(post_data=None, big_post_data=None) -> list:
    """
    Function returns list of dictionaries with tech news
    :param post_data: soup object
    :param big_post_data:
    :return: list of dictionaries
    """
    if not post_data or not big_post_data:
        post_data, big_post_data = find_tech_news_data()
    tech_news = []
    for el in post_data:
        item_news = {'created': el.find('div', class_='post-date').text.strip(), 'title': el.find('a').text.strip(),
                     'link': el.find('a').get('href')}
        tech_news.append(item_news)
    for el in big_post_data:
        news_item = {'created': el.find('div', class_='post-date web-view').text.strip(),
                     'title': el.find('a').text.strip(), 'link': el.find('a').get('href')}
        tech_news.append(news_item)
    return tech_news


def find_python_books_data() -> list:
    """
    Function returns soup object with python books
    :return: soup object
    """
    response = requests.get(URL['python_books'], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    books_data = soup.select('table[class="tableList js-dataTooltip"] tr[itemtype="http://schema.org/Book"]')
    return books_data


def scrapy_python_books(books_data=None) -> list:
    """
    Function returns list of dictionaries with python books
    :param books_data: soup object
    :return: list of dictionaries
    """
    if books_data is None:
        books_data = find_python_books_data()
    python_books = []
    for el in books_data:
        book_item = {'title': el.find('a', class_='bookTitle').text.strip(),
                     'author': el.find('span', itemtype='http://schema.org/Person').text.strip(),
                     'rating': el.find('span', class_='minirating').text.strip()}
        rel_link = el.find('a', class_='bookTitle').get('href')
        book_item['link'] = 'https://www.goodreads.com' + rel_link
        book_item['image'] = el.find('img').get('src')
        python_books.append(book_item)
    return python_books


def find_currency_data(full_url: str) -> list:
    """
    Function returns soup object with currency data
    :param full_url: url for currency
    :return: soup object
    """
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    currency_data = soup.find('tbody', class_='list').find_all('tr')
    return currency_data


def scrapy_currency(currency, date) -> list:
    """
    Function returns list of dictionaries with currency data
    :param currency: currency name
    :param date: date
    :return: list of dictionaries
    """
    try:
        act_date = datetime.strptime(str(date), '%Y-%m-%d').date()
    except ValueError:
        act_date = datetime.now().date()
    full_url = f"{URL['currency']}{currency.lower()}/{act_date}/"
    currency_data = find_currency_data(full_url)
    currency_list = []
    for index, el in enumerate(currency_data):
        currency_item = {'bank': el.find('a', {'class': 'mfm-black-link'}).text.strip()}
        sub_link = el.find('a', {'class': 'mfm-black-link'}).get('href')
        currency_item['link'] = 'https://minfin.com.ua' + sub_link
        currency_item['buy'] = el.find('td', class_='responsive-hide mfm-text-right mfm-pr0').text.strip()
        currency_item['sell'] = el.find('td', class_='responsive-hide mfm-text-left mfm-pl0').text.strip()
        if len(currency_item['buy']) == 0 or len(currency_item['sell']) == 0:
            currency_item['buy'] = '0.0000'
            currency_item['sell'] = '0.0000'
        currency_item['update'] = el.find('td', class_='respons-collapsed mfcur-table-refreshtime').text.strip()
        if index == 10:
            break
        currency_list.append(currency_item)
    return currency_list

