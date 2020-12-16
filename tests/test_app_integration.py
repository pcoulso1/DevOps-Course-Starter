import pytest
from unittest import mock
from dotenv import load_dotenv, find_dotenv

# Use our test integration config instead of the 'real' version 
file_path = find_dotenv('.env.test')
load_dotenv(file_path, override=True)

import app

@pytest.fixture
def client():
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def mock_get_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.trello.com/1/members/me/boards':
        return MockResponse([{'name':  'ToDoBoard', 'id': '5efcab159cb8857fd8fd843e'}], 200)
    elif args[0] == 'https://api.trello.com/1/boards/5efcab159cb8857fd8fd843e/lists':
        return MockResponse([
            {'cards': [
                {'id': '5efcab153d4408623d3a0481', 'name': 'Test task1', 'desc': 'Test in todo', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0482', 'name': 'Test task2', 'desc': 'Test in todo', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0483', 'name': 'Test task3', 'desc': 'Test in todo', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
            ], 'id': '5efcab150107d87d522bd67e', 'name': 'ToDo' }, 
            {'cards': [
                {'id': '5efcab153d4408623d3a0484', 'name': 'Test task4', 'desc': 'Test in in-progress', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0485', 'name': 'Test task5', 'desc': 'Test in in-progress', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0486', 'name': 'Test task6', 'desc': 'Test in in-progress', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
            ], 'id': '5efcd76d91fca074c0cdd75c', 'name': 'InProgress' }, 
            {'cards': [
                {'id': '5efcab153d4408623d3a0487', 'name': 'Test task7', 'desc': 'Test in done', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0488', 'name': 'Test task8', 'desc': 'Test in done', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
                {'id': '5efcab153d4408623d3a0489', 'name': 'Test task9', 'desc': 'Test in done', 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
            ], 'id': '5efcab151352db7d512a1470', 'name': 'Done' }
        ], 200)
    elif args[0] == 'https://api.trello.com/1/cards/5efcab153d4408623d3a0481':
        return MockResponse([
                {'id': '5efcab153d4408623d3a0481', 'name': 'Test task1', 'desc': 'Test in todo', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
        ], 200)


    return MockResponse(None, 404)

def mock_put_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.trello.com/1/cards/5efcab153d4408623d3a0481':
        return MockResponse([{'id': '5efcab153d4408623d3a0484', 'name': 'Test task4', 'desc': 'Test in in-progress', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'}], 200)

    return MockResponse(None, 404)

def mock_post_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.trello.com/1/cards/5efcab153d4408623d3a0481':
        return MockResponse([{'id': '5efcab153d4408623d3a0484', 'name': 'Test task4', 'desc': 'Test in in-progress', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'}], 200)

    return MockResponse(None, 404)

def mock_delete_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.trello.com/1/cards/5efcab153d4408623d3a0481':
        return MockResponse([{'id': '5efcab153d4408623d3a0484', 'name': 'Test task4', 'desc': 'Test in in-progress', 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'}], 200)

    return MockResponse(None, 404)


@mock.patch('requests.get', side_effect=mock_get_requests)
def test_default_endpoint(mock_get_requests, client):
    #given

    # when
    response = client.get("/")
    response_html = response.data.decode()

    # then 
    assert response.status_code == 200
    assert "<title>To-Do App</title>" in response_html
    assert "<h2>Items</h2>" in response_html
    assert "Test task1" in response_html
    assert "Test task2" in response_html
    assert "Test task3" in response_html
    assert "Test task4" in response_html
    assert "Test task5" in response_html
    assert "Test task6" in response_html
    assert "Test task7" in response_html
    assert "Test task8" in response_html
    assert "Test task9" in response_html

@mock.patch('requests.get', side_effect=mock_get_requests)
@mock.patch('requests.put', side_effect=mock_put_requests)
def test_update_endpoint(mock_get_requests, mock_put_requests, client):
    #given

    # when
    response = client.post("/update/5efcab153d4408623d3a0481/InProgress", follow_redirects=False)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

def test_add_get_endpoint(client):
    #given

    # when
    response = client.get("/add", )
    response_html = response.data.decode()

    # then 
    assert response.status_code == 200
    assert "<title>To-Do App</title>" in response_html
    assert "<h2>Add New Items</h2>" in response_html

@mock.patch('requests.get', side_effect=mock_get_requests)
@mock.patch('requests.post', side_effect=mock_post_requests)
def test_add_post_endpoint(mock_get_requests, mock_post_requests, client):
    #given
    form = dict( 
        add='', 
        new_todo_title='Test task1', 
        new_todo_description='Test in in-progress',
        new_todo_due='2020-08-02T04:00:00.000Z')

    # when
    response = client.post("/add", data = form)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

@mock.patch('requests.get', side_effect=mock_get_requests)
def test_delete_get_endpoint(mock_get_requests, client):
    #given

    # when
    response = client.get("/delete/5efcab153d4408623d3a0481")
    response_html = response.data.decode()

    # then 
    assert response.status_code == 200
    assert "<title>To-Do App</title>" in response_html
    assert "<h2>Remove an Item</h2>" in response_html

@mock.patch('requests.delete', side_effect=mock_delete_requests)
def test_delete_post_endpoint(mock_delete_requests, client):
    #given
    form = dict(delete='')

    # when
    response = client.post("/delete/5efcab153d4408623d3a0481", data = form)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

