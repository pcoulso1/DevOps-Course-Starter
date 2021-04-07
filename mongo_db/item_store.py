import os
import pymongo
import datetime
from status import Status
from bson.objectid import ObjectId
from item import Item
from mongo_db.store import Store
class ItemStore(Store):

    COLLECTION_NAME = 'items'

    def __init__(self):
        Store.__init__(self)


    def get_collection(self):
        """
        Fetches all saved items from the Mongo DB.

        Returns:
            list: The list of saved items.
        """

        db = self.get_mongodb()
        return db[ItemStore.COLLECTION_NAME]


    def get_items(self):
        """
        Fetches all saved items from the Mongo DB.

        Returns:
            list: The list of saved items.
        """
        items = [Item.from_json(card) for card in self.get_collection().find()]

        items = sorted(items, key=lambda kv: kv.id)
        items = sorted(items, key=lambda kv: kv.status, reverse=True)

        return items


    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == ObjectId(id)), None)


    def add_item(self, title, description, due):
        """
        Adds a new item with the specified title, description and due date to Mongo DB.

        Args:
            title: The title of the item.
            description: The items description
            due: The date when the item is due

        Returns:
            id: The new saved item id.
        """
        post = {
            'name': title,
            'desc': description,
            'status': Status.TODO,
            'due': due,
            'updated': datetime.datetime.utcnow()}

        return self.get_collection().insert_one(post).inserted_id


    def update_item(self, id, next_status):
        """
        Update the status of an existing item in Mongo DB.

        Args:
            id: The id of the item to updated.

        Returns:
            id: The updated item id or None if it does not exist.
        """
        query = {"_id": ObjectId(id)}
        doc = self.get_collection().find_one(query)
        if doc is not None:
            post = { "$set": {
                'status': next_status,
                'updated': datetime.datetime.utcnow()} }
            
            return self.get_collection().update_one(query, post)
            
        return None


    def edit_item(self, id, title, description, due):
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
        query = {"_id": ObjectId(id)}
        doc = self.get_collection().find_one(query)
        if doc is not None:
            post = { "$set": {
                'name': title,
                'desc': description,
                'due': due,
                'updated': datetime.datetime.utcnow()} }
            
            return self.get_collection().update_one(query, post)

        return None


    def remove_item(self, id):
        """
        Removes an existing item from Mongo DB.

        Args:
            id: The id of the item to remove.

        Returns:
            response: from the api call.
        """
        doc = self.get_collection().find_one({"_id": ObjectId(id)})
        if doc is not None:
            return self.get_collection().delete_one({"_id": ObjectId(id)})

        return None