from status import Status
class Item:

    def __init__(self, id, title, status='ToDo', description='', due=''):
        self.id = id
        self.title = title
        self.description = description
        self.due = due
        self.status = status

    def can_delete(self):
        """
        Returns if the Item is in the correct state to be  deleted
    
        Returns:
            bool: An instance of the Item class.
        """
        return self.status == 'Done'

    def next_status(self):
        """
        Returns the next logical state the item can can be moved to
    
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

    @classmethod
    def from_card(cls, card, card_list):
        """
        Initialize an Item from an instance of a trello card
    
        Args:
            card: The trello card object.
            card_list: The trello card list object which the card belongs to.

        Returns:
            cls: An instance of the Item class.
        """
        return cls(card['id'], card['name'], card_list['name'],card['desc'], card['due'])

