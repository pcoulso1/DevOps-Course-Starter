import os
import pymongo
import datetime
from status import Status
from bson.objectid import ObjectId
from item import Item
from mongo_config import Config

"""
A Global to be used to cache the board ID
"""
MONGODB_CLIENT = None
MONGODB_DATABASE = None

def get_mongodb(db_name=Config().MONGO_DEFAULT_DATABASE):
    """
    Returns the MongoDB

    Returns:
        db: The Mongo DB database object.
    """
    global MONGODB_DATABASE
    if MONGODB_DATABASE is None:
        global MONGODB_CLIENT
        if MONGODB_CLIENT is None:
            MONGODB_CLIENT = pymongo.MongoClient(
                f'mongodb+srv://{Config().MONGO_USER_NAME}:{Config().MONGO_PASSWORD}@{Config().MONGO_HOST}/{db_name}?retryWrites=true&w=majority')
        MONGODB_DATABASE = MONGODB_CLIENT[db_name]

    return MONGODB_DATABASE


def get_lists(db):
    """
    Fetches all lists which exist in the database.

    Returns:
        list: The name of all the list in the DB.
    """
    return db.list_collection_names()


def get_items():
    """
    Fetches all saved items from the Mongo DB.

    Returns:
        list: The list of saved items.
    """
    db = get_mongodb()
    item_lists = get_lists(db)

    items = [Item.from_json(card, item_list)
             for item_list in item_lists
             for card in db[item_list].find()]

    items = sorted(items, key=lambda kv: kv.id)
    items = sorted(items, key=lambda kv: kv.status, reverse=True)

    return items


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == ObjectId(id)), None)


def add_item(title, description, due):
    """
    Adds a new item with the specified title, description and due date to Mongo DB.

    Args:
        title: The title of the item.
        description: The items description
        due: The date when the item is due

    Returns:
        id: The new saved item id.
    """
    db = get_mongodb()
    todo_list = db[Status.TODO]

    post = {
        'name': title,
        'desc': description,
        'status': Status.TODO,
        'due': due,
        'dateLastActivity': datetime.datetime.utcnow()}

    return todo_list.insert_one(post).inserted_id


def update_item(id, next_status):
    """
    Update the status of an existing item in Mongo DB.

    Args:
        id: The id of the item to updated.

    Returns:
        id: The updated item id or None if it does not exist.
    """
    db = get_mongodb()
    item_lists = get_lists(db)

    for item_list in item_lists:
        card = db[item_list].find_one({"_id": ObjectId(id)})
        if card is not None:
            post = {
                'name': card['name'],
                'desc': card['desc'],
                'status': next_status,
                'due': card['due'],
                'dateLastActivity': datetime.datetime.utcnow()}

            new_id = db[next_status].insert_one(post).inserted_id
            db[item_list].delete_one({"_id": ObjectId(id)})
            return new_id

    return None

def edit_item(id, title, description, due):
    """
    Edit an existing items details - title, description and due date to Mongo DB.

    Args:
        id: The id of the item to updated.
        title: The title of the item.
        description: The items description
        due: The date when the item is due

    Returns:
        item: The edited item id or None if it does not exist.
    """
    db = get_mongodb()
    item_lists = get_lists(db)

    query = {"_id": ObjectId(id)}
    for item_list in item_lists:
        card = db[item_list].find_one(query)
        if card is not None:
            post = { "$set": {
                'name': title,
                'desc': description,
                'status': item_list,
                'due': due,
                'dateLastActivity': datetime.datetime.utcnow()} }
            
            return db[item_list].update_one(query, post)

    return None


def remove_item(id):
    """
    Removes an existing item from Mongo DB.

    Args:
        id: The id of the item to remove.

    Returns:
        response: from the api call.
    """
    db = get_mongodb()
    item_lists = get_lists(db)

    for item_list in item_lists:
        card = db[item_list].find_one({"_id": ObjectId(id)})
        if card is not None:
            return db[item_list].delete_one({"_id": ObjectId(id)})

    return None


def setup_test_store():
    """
    Sets a test board ID which is to be used for testing purposes

    Returns:
        None

    """
    reset_store()
    get_mongodb("testBoard")


def reset_store():
    """
    Resets the test store

    Returns:
        None
    """
    global MONGODB_DATABASE
    MONGODB_DATABASE = None
    global MONGODB_CLIENT
    MONGODB_CLIENT = None
