import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from ..libs.scrapy_headers import headers

from ...scrapping.libs.scrapy_urls import URL


# Create your tests here.

class ScrappingTestCase(TestCase):
    """ This test class checks the status code of the response and soup title of the scraped pages"""

    def test_get_news_scrape(self):
        response = requests.get(URL['ukrainian_news'])
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Останні новини України', soup.title.text)

    def test_get_sport_news_scrape(self):
        response = requests.get(URL['sport_news'])
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Свіжі новини спорту онлайн', soup.title.text)

    def test_get_tech_news_scrape(self):
        response = requests.get(URL['tech_news'])
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertGreater(len(soup), 0)

    def test_get_python_books_scrape(self):
        response = requests.get(URL['python_books'])
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Best Python programming books', soup.title.text)

    def test_currency_scrape(self):
        response = requests.get(URL['currency'], headers=headers)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Курс валют в банках України', soup.head.title.text)

