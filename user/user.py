from flask_login import UserMixin

from user.user_role import UserRole

class User(UserMixin):

    def __init__(self, name, id, login, email, role, updated=''):
        self.name = name
        self.id = id
        self.login = login
        self.email = email
        self.role = role
        self.updated = updated

    @property
    def is_readonly(self):
        return self.role == UserRole.READER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @classmethod
    def from_json(cls, json):
        """
        Initialize an User from an instance of the json
    
        Args:
            json: The user in json format.

        Returns:
            cls: An instance of the User class.
        """
        return cls(id=json["id"], login=json["login"], name=json["name"], email=json["email"], role=json.get("role", UserRole.READER), updated=json.get("updated") )

