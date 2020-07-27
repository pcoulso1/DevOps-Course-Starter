import pytest

from item import Item
from status import Status
from view_model import ViewModel
from datetime import date, datetime


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


def test_show_all_done_false():
    #given
    items = [
        Item("id", "title", Status.TODO, "description", "26/09/2020" ),
        Item("id", "title", Status.IN_PROGRESS, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 8
    assert len(vm.todo_items) == 1
    assert len(vm.in_progress_items) == 1
    assert len(vm.done_items) == 6
    assert vm.show_all_done_items == False

def test_show_all_done_true():
    #given
    items = [
        Item("id", "title", Status.TODO, "description", "26/09/2020" ),
        Item("id", "title", Status.IN_PROGRESS, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020" )
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 6
    assert len(vm.todo_items) == 1
    assert len(vm.in_progress_items) == 1
    assert len(vm.done_items) == 4
    assert vm.show_all_done_items == True

def test_recent_done_items():
    #given
    items = [
        Item("id", "title", Status.TODO, "description", "26/09/2020",),
        Item("id", "title", Status.IN_PROGRESS, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2000, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2003, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2005, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' ),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 7
    assert len(vm.todo_items) == 1
    assert len(vm.in_progress_items) == 1
    assert len(vm.done_items) == 5
    assert len(vm.recent_done_items) == 2

def test_older_done_items():
    #given
    items = [
        Item("id", "title", Status.TODO, "description", "26/09/2020",),
        Item("id", "title", Status.IN_PROGRESS, "description", "26/09/2020" ),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2000, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2003, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime(2005, 6, 15, 9, 0, 0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' ),
        Item("id", "title", Status.DONE, "description", "26/09/2020", datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
    ]

    #when
    vm = ViewModel(items)

    #then
    assert len(vm.items) == 7
    assert len(vm.todo_items) == 1
    assert len(vm.in_progress_items) == 1
    assert len(vm.done_items) == 5
    assert len(vm.older_done_items) == 3
