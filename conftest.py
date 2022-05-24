"""
Встроенная фикстура request может получать данные о текущем запущенном тесте, что позволяет, например, сохранять
дополнительные данные в отчёт, а также делать многие другие интересные вещи. В этом шаге мы хотим показать, как можно
настраивать тестовые окружения с помощью передачи параметров через командную строку.

Допустим, нам надо чтобы тест def test_guest_should_see_login_link(browser) мог принимать разные браузеры через командную строку.
Т.е. нам надо ввести дополнительный параметр, назовем его , для запуска теста.
1. Для этого добавляем в файл conftest.py наш дополнительный параметр browser_name с помощью функции pytest_addoption и
встроенной фикстуры parser.
2. Перепишем нашу фикстуру browser, в которую добавим как параметр встроенную фикстуру request. С помощью неё
через browser_name = request.config.getoption("browser_name") и получаем значение введенного тестером
доболниельного параметра browser_name

 Давайте сделаем так, чтобы сервер сам решал, какой язык интерфейса нужно отобразить, основываясь на данных браузера.
Браузер передает данные о языке пользователя через запросы к серверу, указывая в Headers (заголовке запроса) параметр
accept-language. Если сервер получит запрос с заголовком {accept-language: ru, en}, то он отобразит пользователю
русскоязычный интерфейс сайта. Если русский язык не поддерживается, то будет показан следующий язык из списка, в данном
случае пользователь увидит англоязычный интерфейс.


Чтобы указать язык браузера с помощью WebDriver, используйте класс Options и метод add_experimental_option, как указано в примере ниже:

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
browser = webdriver.Chrome(options=options)

Для Firefox объявление нужного языка будет выглядеть немного иначе:

fp = webdriver.FirefoxProfile()
fp.set_preference("intl.accept_languages", user_language)
browser = webdriver.Firefox(firefox_profile=fp)
В конструктор webdriver.Chrome или webdriver.Firefox вы можете добавлять разные аргументы, расширяя возможности
тестирования ваших веб-приложений: можно указывать прокси-сервер для контроля сетевого трафика или запускать разные
версии браузера, указывая локальный путь к файлу браузера. Предполагаем, что эти возможности вам понадобятся позже и
вы сами сможете найти настройки для этих задач.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption('--language', action='store', default=None, help='Choose one of the languages: ar, ca, cs, da, de,'
                                                                      'en-gb, el, es, fi, fr, it, ko,pl, pt, pt-br, ro,'
                                                                      'ru, sk, uk, zh-hans')


@pytest.fixture(scope='function')
def browser(request):
    language = request.config.getoption('language')
    scope_of_languages = ['ar', 'ca', 'cs', 'da', 'de', 'en-gb', 'el', 'es', 'fi', 'fr', 'it', 'ko', 'pl', 'pt',
                          'pt-br', 'ro', 'ru', 'sk', 'uk', 'zh-hans']
    if language in scope_of_languages:
        lang_option = Options()
        lang_option.add_experimental_option('prefs', {'intl.accept_languages': language})
        browser = webdriver.Chrome(options=lang_option)
    else:
        raise pytest.UsageError("--language should be one of the languages: ar, ca, cs, da, de, en-gb, el, es, fi, fr,"
                                "it, ko, pl, pt, pt-br, ro, ru, sk, uk, zh-hans")
    yield browser
    browser.quit()
