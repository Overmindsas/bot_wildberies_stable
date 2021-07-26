import requests
import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pickle
import time
import os
import sqlite3
from threading import Lock
import shutil
import math
import pathlib
from pathlib import Path

def get_html(url):
    r = requests.get(url)
    return r


def after_autorization(url, colvo):
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    option.set_preference('dom.webdriver.enabled', False)
    option.set_preference('general.useragent.ovveride', 'example)')
    browser = webdriver.Firefox(options=option)

    browser.get('https://www.wildberries.ru')

    path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
    path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

    debug = r'G:\python_progs\бот wildberries\cockies'
    prod = r'C:\Users\Хуй\Desktop\бот 1.1\cockies'

    for cookie in pickle.load(open(path2, 'rb')):
        browser.add_cookie(cookie)

    #for cookie in pickle.load(open('G:\python_progs\бот wildberries\cockies', 'rb')):
    #    browser.add_cookie(cookie)

    browser.refresh()
    browser.get(url)

    add_to_basket = '//*[@id="container"]/div[1]/div[2]/div[4]/div[8]/div[1]/button[1]'
    add_to_basket2 = 'div.cart-btn-wrap:nth-child(1) > button:nth-child(1)'
    add_to_baskket3 = '/html/body/div[1]/main/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div[8]/div[1]/button[1]'
    basket = '/html/body/div[1]/header/div/div[2]/div[2]/div[4]/a/span'
    
    button_kolichestvo = '.plus'
    delivery_kura = '//*[@id="basketForm"]/div/div[1]/div[3]/div/div[1]/label[1]'
    
    
    oplata = '//*[@id="basket-footer"]/div/div[4]/button'
    mesto_path = '//*[@id="basketForm"]/div/div[1]/div[3]/div/div[2]/div/div[1]/div/div[2]/div[2]/ul/li/label/span/span[1]'
    
    oplta_pod_path = '/html/body/div[1]/p/div/button'
    browser.get(url)
    try:
        button = browser.find_element_by_xpath(add_to_basket).click()
        time.sleep(1)
    except:
        button = browser.find_element_by_css_selector(add_to_basket2).click()

    button2 = browser.find_element_by_xpath(basket).click()
    time.sleep(3)
    for i in range(colvo-1):
       #button3 = browser.find_element_by_xpath(button_kolichestvo).click()
       button3 = browser.find_element_by_css_selector(button_kolichestvo).click()
    
    #delete_product(url)
    button4 = browser.find_element_by_xpath(delivery_kura).click()
    time.sleep(2)
    button5 = browser.find_element_by_xpath(mesto_path).click()
    time.sleep(2)
    button6 = browser.find_element_by_xpath(oplata).click()
    time.sleep(3)
    button7 = browser.find_element_by_xpath(oplta_pod_path).click()
    time.sleep(2)
    delete_product(url)

    browser.quit()
    open_data_base()



def get_product_wild(html, url, cost_price, money):
    time.sleep(0.5)
    soup = BeautifulSoup(html.text, 'html.parser')
    item = soup.find('span', class_='final-cost').get_text()
    m = ''
    m+=item
    p = re.sub(r'\s', '', m)
    price = p.replace('₽', '')
    print(price)  
    if float(price) <= float(cost_price):
        colvo = int(math.floor((int(money)/int(price))))
        after_autorization(url, colvo)
    else:
        pass
        
     

def add_new_product(url, cost_price, money, description):
    path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
    path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

    debug = r'G:\python_progs\бот wildberries\server.db'
    
    with sqlite3.connect(path) as db:
        
        sql = db.cursor()
        sql.execute(f"SELECT url FROM urlbase WHERE url = '{url}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO urlbase VALUES (?,?,?,?)", (url, cost_price, money, description))
            db.commit()
            print('добавлено')
            
        else:
            print('Этот товар уже есть')

def delete_product(url):
    path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
    path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

    debug = r'G:\python_progs\бот wildberries\server.db'
    
    with sqlite3.connect(path) as db:
        
        sql = db.cursor()
        sql.execute("PRAGMA journal_mode=WAL")
        sql.execute('''DELETE FROM urlbase WHERE url = ?''', (url,))
        db.commit()
    

def show_data_base():
    path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
    path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

    debug = r'G:\python_progs\бот wildberries\server.db'
    

    
    with sqlite3.connect(path) as db:
        
        sql = db.cursor()
        sql.execute("PRAGMA journal_mode=WAL")
        for value in sql.execute("SELECT * FROM urlbase"):
            print('Ссылка: {0}, Себестоимость: {1} , Сумма: {2}, Описание товара: {3}'.format(value[0], value[1], value[2], value[3]))
        print("---------------------------------------------------------------")
        db.commit()
    
def open_data_base():
    while True:
        path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
        path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

        debug = r'G:\python_progs\бот wildberries\server.db'
        

        with sqlite3.connect(path) as db:

            sql = db.cursor()
            sql.execute("PRAGMA journal_mode=WAL")
            for value in sql.execute("SELECT * FROM urlbase"):
                html = get_html(value[0])
                get_product_wild(html, value[0], value[1], value[2])
                db.commit()



def value_data_base():
    path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
    path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')

    debug = r'G:\python_progs\бот wildberries\server.db'
    prod = r'C:\Users\Хуй\Desktop\бот 1.1\server.db'
    with sqlite3.connect(path) as db:
        sql = db.cursor()
        sql.execute("PRAGMA journal_mode=WAL")
        a = sql.execute('''SELECT * FROM urlbase ''')
        b = a.fetchall()
        print(len(b))

