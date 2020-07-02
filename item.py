
class Item:

    def __init__(self, id, title, status='ToDo', description='', due=''):
        self.id = id
        self.title = title
        self.description = description
        self.due = due
        self.status = status

    def can_delete(self):
        return self.status == 'Done'

    def next_status(self):
        if self.status == 'ToDo':
            return 'InProgress'
        elif self.status == 'InProgress':
            return 'Done'
        elif self.status == 'Done':
            return 'ToDo'

    def due_date(self):
        if self.due is not None:
            return self.due
        return ""