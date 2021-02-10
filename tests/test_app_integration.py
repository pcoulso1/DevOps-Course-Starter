import pytest
import mongomock
from bson.objectid import ObjectId
from status import Status
from unittest import mock

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

import app
from mongo_db.config import Config

@pytest.fixture
def client():
    test_app = app.create_app()
    
    with test_app.test_client() as client:
        yield client

def mock_mongoDb_client(*args, **kwargs):

    dbclient = mongomock.MongoClient()
    db = dbclient[Config().MONGO_DEFAULT_DATABASE]

    mockToDoItems = [
        {'_id': ObjectId('5efcab153d4408623d3a0481'), 'name': 'Test task1', 'desc': 'Test in todo',
            'status': Status.TODO, 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0482'), 'name': 'Test task2', 'desc': 'Test in todo', 'status': Status.TODO,
            'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0483'), 'name': 'Test task3', 'desc': 'Test in todo', 'status': Status.TODO,
            'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
    ]
    db[Status.TODO].insert_many(mockToDoItems)

    mockInProgressItems = [
        {'_id': ObjectId('5efcab153d4408623d3a0484'), 'name': 'Test task4', 'desc': 'Test in in-progress',
            'status': Status.IN_PROGRESS, 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0485'), 'name': 'Test task5', 'desc': 'Test in in-progress',
         'status': Status.IN_PROGRESS, 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0486'), 'name': 'Test task6', 'desc': 'Test in in-progress',
         'status': Status.IN_PROGRESS, 'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
    ]
    db[Status.IN_PROGRESS].insert_many(mockInProgressItems)

    mockDoneItems = [
        {'_id': ObjectId('5efcab153d4408623d3a0487'), 'name': 'Test task7', 'desc': 'Test in done',
            'status': Status.DONE, 'due': None, 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0488'), 'name': 'Test task8', 'desc': 'Test in done', 'status': Status.DONE,
         'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'},
        {'_id': ObjectId('5efcab153d4408623d3a0489'), 'name': 'Test task9', 'desc': 'Test in done', 'status': Status.DONE,
         'due': '2020-08-02T04:00:00.000Z', 'dateLastActivity': '2020-07-02T12:59:12.694Z'}
    ]
    db[Status.DONE].insert_many(mockDoneItems)

    return dbclient

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_default_endpoint(mock_mongoDb_client, client):
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

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_update_endpoint(mock_mongoDb_client, client):
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

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_add_post_endpoint(mock_mongoDb_client, client):
    #given
    form = dict( 
        add='', 
        new_todo_title='Test task10', 
        new_todo_description='Test in in-progress',
        new_todo_due='2020-08-02T04:00:00.000Z')

    # when
    response = client.post("/add", data = form)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_edit_get_endpoint(mock_mongoDb_client, client):
    #given

    # when
    response = client.get("/editdetails/5efcab153d4408623d3a0485", )
    response_html = response.data.decode()

    # then 
    assert response.status_code == 200
    assert "<title>To-Do App</title>" in response_html
    assert "<h2>Edit details</h2>" in response_html

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_add_post_endpoint(mock_mongoDb_client, client):
    #given
    form = dict( 
        edit='', 
        todo_title='Test task10', 
        todo_description='Test in in-progress',
        todo_due='2020-08-02T04:00:00.000Z')

    # when
    response = client.post("/editdetails/5efcab153d4408623d3a0485", data = form)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_delete_get_endpoint(mock_mongoDb_client, client):
    #given

    # when
    response = client.get("/delete/5efcab153d4408623d3a0489")
    response_html = response.data.decode()

    # then 
    assert response.status_code == 200
    assert "<title>To-Do App</title>" in response_html
    assert "<h2>Remove an Item</h2>" in response_html

@mock.patch('pymongo.MongoClient', side_effect=mock_mongoDb_client)
def test_delete_post_endpoint(mock_mongoDb_client, client):
    #given
    form = dict(delete='')

    # when
    response = client.post("/delete/5efcab153d4408623d3a0489", data = form)
    response_html = response.data.decode()

    # then 
    assert response.status_code == 302
    assert "<h1>Redirecting...</h1>" in response_html

