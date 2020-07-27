import pytest
# from hypothesis import given
# from hypothesis.strategies import integers
# from selenium import webdriver

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_default_page(client):
    # Use the client to make requests e.g.:
    response = client.get("/")
    
    assert response.status_code == 200

# # Module scope re-uses the fixture
# @pytest.fixture(scope='module')
# def driver():
#     # path to your webdriver download
#     opts = webdriver.ChromeOptions()
#     opts.add_argument('--headless')
    
#     # path to your webdriver download
#     with webdriver.Chrome('C:/Users/pcoul/Documents/CS Dipolma/Module 3/chromedriver_win32/chromedriver', options=opts) as driver:
#         yield driver


# def test_python_home(driver):
#     driver.get("https://www.python.org")
#     assert driver.title == 'Welcome to Python.org'


# @pytest.mark.parametrize('number', [-10, 0, 1, 5, 1000000])
# def test_division(number):
#     assert number / 1 == number


# @given(number=integers())
# def test_division_with_hypothesis(number):
#     assert number / 1 == number
