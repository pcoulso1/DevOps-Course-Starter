from datetime import date, datetime
from status import Status
class Item:

    def __init__(self, id, title, status=Status.TODO, description='', due='', updated=''):
        self.id = id
        self.title = title
        self.description = description
        self.due = due
        self.status = status
        self.updated = updated

    def can_delete(self):
        """
        Returns if the Item is in the correct state to be deleted
    
        Returns:
            bool: An instance of the Item class.
        """
        return self.status == Status.DONE

    def next_status(self):
        """
        Returns the next logical state the item can be moved to
    
        Returns:
            String: The name of the next state the item can be moved to.
        """
        if self.status == Status.TODO:
            return Status.IN_PROGRESS
        elif self.status == Status.IN_PROGRESS:
            return Status.DONE
        elif self.status == Status.DONE:
            return Status.TODO

    def due_date(self):
        """
        Returns due date of the item in the correct format.
    
        Returns:
            String: the due date.
        """
        if self.due is not None:
            return self.due
        return ""

    def done_today(self):
        """
        Returns if the item was modified today and the status is done.
    
        Returns:
            bool: if moved into done state today.
        """
        return self.status == Status.DONE and datetime.strptime(self.updated, '%Y-%m-%dT%H:%M:%S.%fZ').date() == date.today()

    @classmethod
    def from_json(cls, json, listname):
        """
        Initialize an Item from an instance of the bacnking store json
    
        Args:
            json: The todo item in json.
            listname: The name of the list the item belongs to.

        Returns:
            cls: An instance of the Item class.
        """
        return cls(json['_id'], json['name'], listname, json['desc'], json['due'], json['dateLastActivity'])

