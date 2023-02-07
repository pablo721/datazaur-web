
from pycoingecko import CoinGeckoAPI
import requests
import os
import pandas as pd
import datetime
from src.utils.decorators import load_or_save
from datawarehouse.models import Config





filename = 'cryptocomp_news.files'

@load_or_save(filename, 86400)
def cryptocomp_news():
    api_key = '70d54fd6e56db84eba0a9d9166b4d5da087c79d3d6cc0511e69144270f90c09b'
    url = f'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}'
    df = pd.json_normalize(requests.get(url).json()['Data'])[['published_on', 'title', 'url', 'source', 'body',
                                                          'categories']]
    df.loc[:, 'body'] = df.loc[:, 'body'].apply(lambda x: x[:320] + '...')

    df['title'] = df.apply(lambda x: f"""<a href="{x['url']}">{x['title']}</a>""", axis=1)
    df['published_on'] = df['published_on'].apply(lambda x: pd.to_datetime(x * 10 ** 9), True)
    df.drop('url', axis=1, inplace=True)
    df.columns = ['Date', 'Title', 'Source', 'Text', 'Categories']
    return df



@load_or_save('gecko_events.files', 86400)
def gecko_events():
    data = []
    gecko = CoinGeckoAPI()
    events = gecko.get_events()['data']
    for event in events:
        data.append([event['description'], pd.DataFrame(pd.Series(event)).drop('description').transpose().to_html(escape=False, justify='center')])
    return data





def scrap_news():
    result = {}
    for website, selectors in load_websites().items():
        result[website] = []
        req = requests.get(website).text
        soup = BeautifulSoup(req, features='lxml')
        for selector in selectors:
            articles = soup.select(selector)
            #result[website].append([[article.a.text, article.a.get('href')] for article in articles])
            result[website].append(f'<a href="{article.a.get("href")}"> {article.a.text} </a>' for article in articles)

    return result


def add_website(url, selectors):
    if url in load_websites().keys():
        return 'Site already saved.'
    else:
        with open(filename, 'a') as file:
            yaml.dump({url: selectors}, file)
        print('added')



def remove_website(url):
    pass

def set_selector(url):
    pass

