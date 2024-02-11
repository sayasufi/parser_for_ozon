import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs4
from selenium import webdriver

from source.funcs import page_open, func_parse


def search(product_name: str, number_pages: int = 1):
    """Функция, которая возвращает список свойств товаров"""
    driver = webdriver.Chrome()
    list_products = []
    # начальная строка
    url = f"https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text={product_name}"
    for page in range(1, number_pages + 1):
        # добавляем нужную страницу к url и отправляем в функцию pageOpen на скачку
        source_text = page_open(f'{url}&page={page}', driver)

        # удаляем из текста всякие комментарии, чтобы не болтались мертвым грузом. Но это не обязательно
        result = re.sub(r'<!.*?->', '', source_text)
        # создаем обьект bs4, на основе скаченного html
        soup = bs4(result, 'html.parser')
        # Находим нужный нам html обьект по тагу и его id - там хранятся данные о товарах
        items_body = soup.find('div', id='paginatorContent')
        # переходим на нужные теги
        items = items_body.div.div
        # парсим данные
        list_products.extend(func_parse(items=items))

    driver.quit()
    return list_products


def options_parser(row, options_set_in):
    """Функция для парсинга свойств"""
    for option in options_set_in:
        row[option] = (row['options'].get(option))
    return row


def create_excel(product_name: str, number_pages: int = 1):
    """Создание таблица excel со всеми товарами"""

    captured_data = search(product_name, number_pages)

    df = pd.DataFrame(captured_data)

    # Создаем пустой set, куда в процессе поместим все уникальные названия опций
    options_set = set()

    # Получаем уникальные названия опций
    for i in captured_data:
        options_set = set(i['options'].keys()) | options_set

    #  Создаем новые колонки согласно опциям
    for col in options_set:
        df[col] = np.nan

    df = df.apply(options_parser, axis=1, options_set_in=options_set)
    df = df.drop(columns=['options'])
    df.to_csv('ozon_parse.csv')


if __name__ == '__main__':
    create_excel("3070", 1)
