import time

import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from allure_commons.types import AttachmentType

timeout = 10


@pytest.allure.severity(pytest.allure.severity_level.BLOCKER)
@pytest.mark.parametrize('button', [
    {'url': '/qa/addition', 'label': 'Операция сложения'}
])
def test_main_page(browser, button):
    """ Main page. """
    browser.get('http://rulkov.ru/qa/')
    time.sleep(1)
    button_addition = browser.find_element_by_xpath("//a[@href='{}']".format(button['url']))

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    assert button_addition.text == button['label']


@pytest.allure.severity(pytest.allure.severity_level.BLOCKER)
@pytest.mark.parametrize('credentials', [
    {'username': 'WQA', 'password': 12345}
])
def test_login_valid(browser, credentials):
    """ Valid login. """
    browser.get('http://rulkov.ru/qa/#/login')

    wait = WebDriverWait(browser, timeout)
    username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

    username.send_keys(credentials['username'])
    password.send_keys(credentials['password'])

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    browser.find_element_by_xpath("//button[@type='submit']").click()

    # Redirect to Addition page.
    wait.until(EC.title_contains('Калькулятор'))
    assert "Калькулятор" in browser.title


@pytest.allure.severity(pytest.allure.severity_level.BLOCKER)
@pytest.mark.parametrize('credentials', [
    {'username': 'WQA', 'password': 12345}
])
@pytest.mark.parametrize('values', [
    (0, 1, 1000001),
    (1, 1000000, 0),
    (1000000, 0, 1),
])
def test_addition(browser, credentials, values):
    """ Addition works with valid values (positive integers). """
    browser.get('http://rulkov.ru/qa/#/addition')

    wait = WebDriverWait(browser, timeout)
    username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

    username.send_keys(credentials['username'])
    password.send_keys(credentials['password'])

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    browser.find_element_by_xpath("//button[@type='submit']").click()

    # Redirect to Addition page.
    wait.until(EC.title_contains('Калькулятор'))

    # Test addition
    # Stage 1. Input values.
    value1 = wait.until(EC.presence_of_element_located((By.ID, 'value1')))
    value1.send_keys(values[0])
    value2 = wait.until(EC.presence_of_element_located((By.ID, 'value2')))
    value2.send_keys(values[1])
    value3 = wait.until(EC.presence_of_element_located((By.ID, 'value3')))
    value3.send_keys(values[2])

    forward1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Вперед']")))

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    forward1.click()

    # Stage 2. Confirm values.
    wait.until(EC.title_contains('Шаг: 2'))
    row1 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[0]))))
    row2 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[1]))))
    row3 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[2]))))

    forward2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Вперед']")))

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    forward2.click()

    # Stage 3. Show result.
    wait.until(EC.title_contains('Шаг: 4'))
    table = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='calculator']//table")))
    rows = table.find_elements(By.TAG_NAME, "tr")

    row1 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[0]))))
    row2 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[1]))))
    row3 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(values[2]))))
    row3 = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text() = '{}']".format(sum(values)))))

    allure.attach(browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)

    # If the sum of values is even, the row should be green.
    result_class = rows[3].get_attribute("class")
    if sum(values) % 2:
        assert result_class != 'bg-success'
    else:
        assert result_class == 'bg-success'
    forward3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Вернуться к вводу данных']")))
    forward3.click()
