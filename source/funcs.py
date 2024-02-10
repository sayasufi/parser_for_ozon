import os
import pickle
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def page_open(url):
    """Функция, удаляющая предыдущие cookies, подставляющая нужные и получающая конечный результат страницы"""

    driver = webdriver.Chrome()
    driver.get(url)

    if not os.path.exists("session"):
        time.sleep(10)
        pickle.dump(driver.get_cookies(), open("session", "wb"))
        print("Получаем cookies")
        return None
    else:
        driver.delete_all_cookies()
        for cookie in pickle.load(open("session", "rb")):
            driver.add_cookie(cookie)

    # Получаем страницу
    driver.get(url)

    # Ожидаем тега ozonTagManagerApp, указывающий что страница полностью загружена
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ozonTagManagerApp")))
    except TimeoutException:
        return None

    return driver.page_source  # Возвращаем текст страницы


# Функция,
def options_dictionary(options_list: list) -> dict:
    options_dict = {}
    for option in options_list:
        options_dict[option.split(':')[0].strip()] = option.split(':')[1].strip()
    return options_dict


# Функция, вылавливающая данные о картинках
def images_dict(good_id: int, mask: str) -> dict:
    images_dictionary = []
    try:
        # ищем div у которого в атрибуте data-state есть название имени файла
        data = soup.select_one(f'div[data-state*="{mask}"]')['data-state']
        # данные представлены в json формате, так что используем это и преобразуем в словарь
        json_data = json.loads(data)
        # зная структуру json данных, находим в словаре нужные нам данные
        for link in json_data['items'][good_id]['tileImage']['items']:
            images_dictionary.append(link['image']['link'])
        return images_dictionary
    except:
        return []


print(page_open(
    "https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=3070"))
