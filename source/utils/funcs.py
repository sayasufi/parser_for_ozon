import os
import pickle
import re
import time
from typing import Optional

from bs4.element import Tag
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def valid_session(path: str = "session") -> bool:
    """Проверка куки на валидность"""
    if not os.path.exists(path):
        return False
    elif time.time() - os.path.getmtime(path) > 7200:
        os.remove(path)
        return False
    else:
        return True


def page_open(url: str, driver, session_path: str) -> Optional[str]:
    """Функция, удаляющая предыдущие cookies, подставляющая нужные и получающая конечный результат страницы"""

    if not valid_session(session_path):
        driver.get(url)
        time.sleep(10)
        pickle.dump(driver.get_cookies(), open(session_path, "wb"))

    driver.get(url)
    driver.delete_all_cookies()
    for cookie in pickle.load(open(session_path, "rb")):
        driver.add_cookie(cookie)

    # Получаем страницу
    driver.get(url)

    # Ожидаем тега ozonTagManagerApp, указывающий, что страница полностью загружена
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ozonTagManagerApp")))
    except TimeoutException:
        return None

    # Возвращаем текст страницы
    return driver.page_source


# Функция,
def options_dictionary(options_list: list) -> dict:
    """Делаем словарь для свойств товара"""
    options_dict = {}
    for option in options_list:
        options_dict[option.split(':')[0].strip()] = option.split(':')[1].strip()
    return options_dict


def func_parse(items) -> list:
    """Функция для парсинга элементов"""
    captured_data = []
    idx = 0
    # Создаем словарь, куда будем помещать все полученные данные для товара

    for sibling in items:
        if isinstance(sibling, Tag) and sibling.text:
            item = {}
            # Получаем название товара
            item_name = sibling.div.next_sibling.next_sibling.div.a.span.text
            item['name'] = item_name

            # Получаем основную картинку предпросмотра
            img = sibling.div.a.div.div.img['src']
            item['preimage'] = img

            # Получаем ссылку на товар
            ref = "https://www.ozon.ru" + sibling.div.next_sibling.next_sibling.div.a["href"]
            item["ref"] = ref

            # Получаем свойства для товара
            if options := sibling.div.next_sibling.next_sibling.div.select_one('span.tsBody400Small'):
                options_str = str(options)
                # Убираем ненужные теги
                cleaned_str = re.sub(r'<?.span>|<font color="#......">|</font>', '', options_str)
                cleaned_str = re.sub('<span class="tsBody400Small">', '', cleaned_str)
                item_options = options_dictionary(cleaned_str.split('<br/>'))
                item['options'] = item_options
            idx += 1

            # Получаем цену товара
            price = sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.div.span
            price_text = price.text[:-1].replace(' ', '')
            # Перекодируем цену
            item['price'] = int(price_text.encode('ascii', 'ignore'))

            # Добавляем наш товар в список товаров
            captured_data.append(item)

    return captured_data
