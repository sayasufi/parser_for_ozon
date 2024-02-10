import os
import pickle
import time

from selenium import webdriver

def get_cookies(driver):
browser = webdriver.Chrome()
browser.get('https://www.ozon.ru/')

if not os.path.exists("session"):
    time.sleep(10)
    pickle.dump(browser.get_cookies(), open("session", "wb"))
else:
    for cookie in pickle.load(open("session", "rb")):
        browser.add_cookie(cookie)
