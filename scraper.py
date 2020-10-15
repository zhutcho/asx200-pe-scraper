from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import re
import csv
import itertools
import random
from time import sleep


gecko_install = GeckoDriverManager().install()
driver = webdriver.Firefox(executable_path=gecko_install)


def find_data(results, keyword, index):
    data_pos = results.find(keyword)
    data_replace = results[data_pos:data_pos + 1000].replace('<', '>')
    data_splice = data_replace.split('>')[index]
    data = data_splice.strip()
    return data


class Information():
    results = ""
    pe_ttm = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + ticker
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_pe_ttm(find_data(self.results, "Price To Earnings (TTM)", 8))

    def set_results(self, results):
        self.results = results

    def get_pe_ttm(self):
        return self.pe_ttm

    def set_pe_ttm(self, value):
        self.pe_ttm = value


def get_list():
    with open('tickers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(itertools.chain.from_iterable(reader))[1:]
        csvfile.close()
    return data


def to_CSV():
    sleep_count = 0
    ticker_list = get_list()
    with open('asx200_pe_2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["ticker"] + ["pe (ttm)"])
        for ticker in ticker_list:
            sleep_count += 1
            print(str(sleep_count) + '. ' + ticker)
            ticker_information = Information(ticker)
            # sleep(random.random() * 5 + 10)

            pe_ttm = ticker_information.get_pe_ttm()
            writer.writerow([ticker] + [pe_ttm])

            # if sleep_count % 6 == 0:
            #     sleep(random.random() * 120 + 150)
    driver.close()


to_CSV()
