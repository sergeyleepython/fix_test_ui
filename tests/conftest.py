import pytest


def pytest_addoption(parser):
    parser.addoption('--browser', action='store',
                     default='firefox',
                     help="Options: firefox, chrome, edge, safari, phantomjs. Default: firefox.")


@pytest.fixture
def browser(request):
    from selenium.webdriver import Firefox, Chrome, Edge, Safari, PhantomJS
    mapping = {
        'firefox': Firefox,
        'chrome': Chrome,
        'edge': Edge,
        'safari': Safari,
        'phantomjs': PhantomJS
    }
    browser = request.config.getoption("--browser")
    try:
        driver = mapping[browser.lower()]
    except KeyError:
        raise Exception('Your --browser option value is incorrect. Please, refer to --help.')
    driver = driver()
    request.addfinalizer(driver.close)
    return driver
