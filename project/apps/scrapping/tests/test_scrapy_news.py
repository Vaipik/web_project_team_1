from pathlib import Path

import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from ...scrapping.services.scrapy_news import scrapy_ukr_news, scrapy_sport_news, scrapy_tech_news, \
    scrapy_python_books, find_currency_data, scrapy_currency
from ...scrapping.libs.scrapy_headers import headers


# Create your tests here.

class ScrapyNewsTestCase(TestCase):
    """This test class checks if the scraping function saves data to a dictionary."""

    def test_scrapy_ukr_news(self):
        ukr_news_data = [
            {'created': '15:31', 'title': 'news1', 'link': 'https://www.pravda.com.ua/news1'},
        ]

        ukr_news_data_soup = '<div class="article_news_list"><div class="article_time">15:31</div>' \
                             '<div class="article_content"><div class="article_header">' \
                             '<a href="/news1">news1</a></div><div class="article_subheader">' \
                             '</div></div></div>'
        soup = BeautifulSoup(ukr_news_data_soup, 'html.parser')
        news = scrapy_ukr_news(soup)
        self.assertEqual(len(news), 1)
        self.assertEqual(news, ukr_news_data)

    def test_scrapy_sport_news(self):
        sport_news_data = [
            {'created': '16:45', 'title': 'News1', 'category': 'Футбол', 'link': 'https://sport.ua/uk/news/news1'},
        ]

        sport_news_data_soup = '<div class="item"><div class="item-content"><div class="item-row">' \
                               '<span class="item-sport football">Футбол</span><span class="item-line">|</span>' \
                               '<span class="item-date">16:45</span></div>' \
                               '<div class="item-title item-title--b newsline-title">' \
                               '<a href="https://sport.ua/uk/news/news1"><span>News1</span></a></div></div></div>'
        soup = BeautifulSoup(sport_news_data_soup, 'html.parser')
        news = scrapy_sport_news(soup)
        self.assertEqual(len(news), 1)
        self.assertEqual(news, sport_news_data)

    def test_scrapy_tech_news(self):
        tech_news_data = [
            {'created': '17:02', 'title': 'News1', 'link': 'https://ain.ua/post-list/news1'},
            {'created': '17:05', 'title': 'News2', 'link': 'https://ain.ua/post-list/news2'},
        ]

        path = Path(__file__).parent / 'test_libs' / 'test_tech_news_data.html'
        with open(path, encoding='utf-8') as html:
            tech_news_data_soup = html.read()
        soup = BeautifulSoup(tech_news_data_soup, 'html.parser')
        post_data = soup.find_all('li', class_='post-item ordinary-post')
        big_post_data = soup.find_all('div', class_='big-post-preview')
        news = scrapy_tech_news(post_data, big_post_data)
        self.assertEqual(len(news), 2)
        self.assertEqual(news, tech_news_data)

    def test_scrapy_python_books(self):
        python_books_data = [
            {'title': 'Some python Book', 'author': 'Famous author', 'rating': '5 avg rating',
             'link': 'https://www.goodreads.com/some-python-book',
             'image': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1111.jpg'},
        ]
        path = Path(__file__).parent / 'test_libs' / 'test_python_books_data.html'
        with open(path, encoding='utf-8') as f:
            python_books_data_soup = f.read()
        soup = BeautifulSoup(python_books_data_soup, 'html.parser')
        books = scrapy_python_books(soup)
        self.assertEqual(len(books), 1)
        self.assertEqual(books, python_books_data)


class ScrapyCurrencyTestCase(TestCase):
    """This test class checks if the scraping function saves currency data to a dictionary."""

    def test_scrapy_currency(self):
        currency = 'USD'
        date = '2023-02-07'
        result = scrapy_currency(currency, date)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIn('bank', item)
            self.assertIn('link', item)
            self.assertIn('buy', item)
            self.assertIn('sell', item)
            self.assertIn('update', item)
