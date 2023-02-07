import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
import requests
import time
import numpy as np
import pandas as pd
import os
from pathlib import Path

url = 'https://dappradar.com/nft/collections/'
links = [url + str(n) for n in range(1, 150)]
selector = '.sc-iLOkMM'


def clean(text):
    for word in ['INFO', 'NEW']:
        if word in text:
            text = text.replace(word, '')
    return text


def wait(secs=10, offset=2):
    return secs + (np.random.rand(offset)[0] - offset/2) + np.random.rand(1)[0]


def main():
    driver = webdriver.Firefox()
    nfts = []
    try:
        for link in links:
            driver.get(link)
            names = driver.find_elements('css selector', selector)
            clean_names = list(map(clean, [name.text for name in names]))
            nfts += clean_names
            t = wait()
            time.sleep(t)
            print(nfts)
            print(t)
    except Exception as e:
        print(f'error {e}')
    finally:
        df = pd.DataFrame(columns=['NFT'], data={'NFT': nfts})
        df.to_csv('nftki.files')

        print('done')




if __name__ == '__main__':
    main()

