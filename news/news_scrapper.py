from bs4 import BeautifulSoup

import requests
import yaml
import os
import sys
from datawarehouse.models import Config
from .models import Website




def scrap_website(url, selector, pages=None):
    req = requests.get(url).text
    soup = BeautifulSoup(req, features='lxml')
    articles = soup.select(selector)
    return [article.a for article in articles]


def scrap_all_websites():
    results = {}
    for website in Website.objects.all():
        site_news = []
        for selector in website.selectors.all():
            news = scrap_website(url=website.url, selector=selector.text)
            site_news += news
        results[website.url] = site_news
    print(f'Scrapped: {results}')
    return results




