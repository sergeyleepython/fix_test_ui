import time

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

timeout = 10


@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@pytest.mark.parametrize('credentials', [
    {'username': 'invalid_username', 'password': 'invalid_password'},
    {'username': '', 'password': ''}
])
def test_login_invalid(browser, credentials):
    """ Invalid login. """
    browser.get('http://rulkov.ru/qa/#/login')

    wait = WebDriverWait(browser, timeout)
    username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

    username.send_keys(credentials['username'])
    password.send_keys(credentials['password'])

    browser.find_element_by_xpath("//button[@type='submit']").click()

    time.sleep(3)

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    # Shouldn't redirect to Addition page.
    assert "Калькулятор" not in browser.title
