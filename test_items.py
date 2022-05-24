from selenium.webdriver.common.by import By
import time


link = 'http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'


def test_languages(browser):
    browser.get(link)
    # time.sleep(30)
    browser.implicitly_wait(5)
    btn_add_to_basket = browser.find_elements(By.CSS_SELECTOR, '.btn-add-to-basket')
    print(browser.find_elements(By.CSS_SELECTOR, '.btn-add-to-basket'))
    assert btn_add_to_basket, "The button of add to basket is not found!"
