import datetime

from mongo_db.store import Store
from bson.objectid import ObjectId
from user.user import User
from user.user_role import UserRole

class UserStore(Store):

    COLLECTION_NAME = 'users'

    def __init__(self):
        Store.__init__(self)


    def get_collection(self):
        """
        Fetches all saved items from the Mongo DB.

        Returns:
            list: The list of saved items.
        """

        db = self.get_mongodb()
        return db[UserStore.COLLECTION_NAME]


    def get_users(self):
        """
        Fetches all saved users from the Mongo DB.

        Returns:
            list: The list of saved users.
        """
        users = [User.from_json(json) for json in self.get_collection().find()]

        users = sorted(users, key=lambda kv: kv.id)

        return users

    def get_user(self, user_id):
        """
        Fetches the saved user with the specified ID.

        Args:
            id: The ID of the user.

        Returns:
            user: The saved user, or None if no user match the specified ID.
        """
        users = self.get_users()
        return next((user for user in users if user.id == int(user_id)), None)
    
    def add_user_if_missing(self, user):
        """
        Adds a new user to Mongo DB.

        Args:
            user: The user to save

        Returns:
            id: The new saved item id.
        
        """
        users = self.get_users()

        if(users is None or len(users) == 0):
            post = {
                'id': user.id,
                'name': user.name,
                'login': user.login,
                'email': user.email,
                'role': UserRole.ADMIN,
                'updated': datetime.datetime.utcnow()}

            return self.get_collection().insert_one(post).inserted_id
        else:
            stored_user = next((user for user in users if user.id == int(user.id)), None)
            if(stored_user is None):
                post = {
                    'id': user.id,
                    'name': user.name,
                    'login': user.login,
                    'email': user.email,
                    'role': user.role,
                    'updated': datetime.datetime.utcnow()}

                return self.get_collection().insert_one(post).inserted_id
        
        return None
        
    def update_user(self, id, role):
        """
        Update the role of an existing user in Mongo DB.

        Args:
            id: The id of the user to updated.

        Returns:
            id: The updated user id or None if it does not exist.
        """
        query = {"id": int(id)}
        doc = self.get_collection().find_one(query)
        if doc is not None:
            post = { "$set": {
                'role': role,
                'updated': datetime.datetime.utcnow()} }
            
            return self.get_collection().update_one(query, post)
            
        return None

    def remove_user(self, id):
        """
        Removes an existing user from Mongo DB.

        Args:
            id: The id of the user to remove.

        Returns:
            response: from the api call.
        """
        doc = self.get_collection().find_one({"id": int(id)})
        if doc is not None:
            return self.get_collection().delete_one({"id": int(id)})

        return None

