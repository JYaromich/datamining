from selenium import webdriver #библиотека взаимодействия с web driver broser
from selenium.webdriver.common.keys import Keys #значения клавиш


if __name__ == '__main__':
    url = 'https://habr.com/ru/'
    browser = webdriver.Firefox() # инициализация браузера
    browser.get(url)
    print(1)
