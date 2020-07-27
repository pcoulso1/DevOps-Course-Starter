from status import Status

class ViewModel:

    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == Status.TODO]
    
    @property
    def in_progress_items(self):
        return [item for item in self._items if item.status == Status.IN_PROGRESS]

    @property
    def done_items(self):
        return [item for item in self._items if item.status == Status.DONE]
