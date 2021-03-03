import pytest
import os
from threading import Thread 
from unittest import mock

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

import app
from mongo_db.item_store import ItemStore

from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable

    # Setup the test boards
    item_store = ItemStore()
    item_store.setup_test_store()

    # construct the new application
    application = app.create_app(item_store) 
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    
    # Tear Down
    thread.join(1)

    # Reset the item store internal stat
    item_store.reset_store()

@pytest.fixture(scope='module')
def driver():
    # path to your webdriver download
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    
    # path to your webdriver download
    with webdriver.Chrome('chromedriver', options=opts) as driver:
        yield driver

def test_home(driver, test_app):
    # givenpytest --cov-report term 

    # when
    driver.get('http://localhost:5000/')

    # then
    rowCount = len(driver.find_elements_by_xpath("//table[@id='todo-table']/tbody/tr"))
    assert driver.title == 'To-Do App'
    assert rowCount == 1

def test_add_element(driver, test_app):
    # given
    driver.get('http://localhost:5000/')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()

    # when
    new_task_title_input = driver.find_element_by_xpath("//*[@name='new_todo_title']")
    new_task_title_input.send_keys('Test Task')
    new_task_description_input = driver.find_element_by_xpath("//*[@name='new_todo_description']")
    new_task_description_input.send_keys('Test Task Description')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()

    # then
    rowCount = len(driver.find_elements_by_xpath("//table[@id='todo-table']/tbody/tr"))

    assert driver.title == 'To-Do App'
    assert rowCount == 2

    # cleanup
    driver.find_element_by_xpath("//button[contains(text(), 'Start Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Finish Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove Task')]").click()

def test_edit_element(driver, test_app):
    # given
    driver.get('http://localhost:5000/')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()
    new_task_title_input = driver.find_element_by_xpath("//*[@name='new_todo_title']")
    new_task_title_input.send_keys('Test Task')
    new_task_description_input = driver.find_element_by_xpath("//*[@name='new_todo_description']")
    new_task_description_input.send_keys('Test Task Description')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()

    # when
    driver.find_element_by_xpath("//button[contains(text(), 'Edit')]").click()
    new_task_title_input = driver.find_element_by_xpath("//*[@name='todo_title']")
    new_task_title_input.send_keys('New Test Task title')
    new_task_description_input = driver.find_element_by_xpath("//*[@name='todo_description']")
    new_task_description_input.send_keys('New Test Task Description')
    driver.find_element_by_xpath("//button[contains(text(), 'Edit Task')]").click()

    # then
    rowCount = len(driver.find_elements_by_xpath("//table[@id='todo-table']/tbody/tr"))

    assert driver.title == 'To-Do App'
    assert rowCount == 2

    # cleanup
    driver.find_element_by_xpath("//button[contains(text(), 'Start Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Finish Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove Task')]").click()


def test_delete_element(driver, test_app):
    # given
    driver.get('http://localhost:5000/')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()
    new_task_title_input = driver.find_element_by_xpath("//*[@name='new_todo_title']")
    new_task_title_input.send_keys('Test Task')
    new_task_description_input = driver.find_element_by_xpath("//*[@name='new_todo_description']")
    new_task_description_input.send_keys('Test Task Description')
    driver.find_element_by_xpath("//button[contains(text(), 'Add Task')]").click()

    # when
    driver.find_element_by_xpath("//button[contains(text(), 'Start Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Finish Task')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Remove Task')]").click()

    # then
    rowCount = len(driver.find_elements_by_xpath("//table[@id='todo-table']/tbody/tr"))

    assert driver.title == 'To-Do App'
    assert rowCount == 1