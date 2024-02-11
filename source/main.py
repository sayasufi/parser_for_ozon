import argparse
import logging
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs4
from environs import Env
from selenium import webdriver

from utils.funcs import page_open, func_parse
from logs.setup_logging import setup_logging


def search(product_name: str, number_pages: int = 1):
    """Функция, которая возвращает список свойств товаров"""
    driver = webdriver.Chrome()
    list_products = []
    # начальная строка
    url = f"https://www.ozon.ru/search/?text={product_name}&from_global=true"
    for page in range(1, number_pages + 1):
        # добавляем нужную страницу к url и отправляем в функцию pageOpen на скачку
        source_text = page_open(f'{url}&page={page}', driver, "utils/session")

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
        logging.info(f"Страниц пропаршено: {page} / {number_pages}")

    driver.quit()
    return list_products


def options_parser(row, options_set_in):
    """Функция для парсинга свойств"""
    for option in options_set_in:
        row[option] = (row['options'].get(option))
    return row


def create_excel(product_name: str, number_pages: int = 1, percentage: int = 20):
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
    # Расчет процента заполненных ячеек для каждого столбца
    filled_percentage = df.count() / len(df) * 100

    # Фильтрация столбцов по условию
    filtered_columns = filled_percentage[filled_percentage >= percentage].index

    # Удаление ненужных столбцов
    df_filtered = df[filtered_columns]

    df_filtered.to_csv('ozon_parse.csv')
    logging.info("Таблица сохранена в файл ozon_parse.csv")


if __name__ == '__main__':

    setup_logging("logs/cache.log")
    env = Env()
    env.read_env("utils/.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Имя файла Excel", default=env("NAME"))
    parser.add_argument("--pages", type=int, help="Количество строк", default=int(env("NUMBER_OF_PAGES")))
    parser.add_argument("--threshold", type=int, help="Пороговое значение процента заполненных ячеек",
                        default=int(env("FILTER")))
    args = parser.parse_args()

    create_excel(args.name, args.pages, args.threshold)
