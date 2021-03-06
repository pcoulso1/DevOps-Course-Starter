from status import Status

class ItemsViewModel:

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
 
    @property
    def show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.done_today()]
        
    @property
    def older_done_items(self):
        return [item for item in self.done_items if not item.done_today()]
        
 