import pytest

from item import Item
from status import Status
from view_model import ViewModel


def test_todo_status():
    #given
    items = [
        Item("id", "title", Status.TODO, "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 1
    assert len(vm.todo_items) == 1
    assert len(vm.in_progress_items) == 0
    assert len(vm.done_items) == 0
    
def test_in_progress_status():
    #given
    items = [
        Item("id", "title", Status.IN_PROGRESS, "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 1
    assert len(vm.todo_items) == 0
    assert len(vm.in_progress_items) == 1
    assert len(vm.done_items) == 0

def test_done_status():
    #given
    items = [
        Item("id", "title", Status.DONE, "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 1
    assert len(vm.todo_items) == 0
    assert len(vm.in_progress_items) == 0
    assert len(vm.done_items) == 1

def test_unknown_status():
    #given
    items = [
        Item("id", "title", "unknown", "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 1
    assert len(vm.todo_items) == 0
    assert len(vm.in_progress_items) == 0
    assert len(vm.done_items) == 0