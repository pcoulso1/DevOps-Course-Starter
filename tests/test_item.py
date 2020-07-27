import pytest

from item import Item
from status import Status

def test_can_delete_done_state():
    #given
    status = Status.DONE

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.can_delete() == True

def test_can_delete_todo_state():
    #given
    status = Status.TODO

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.can_delete() == False

def test_can_delete_in_progress_state():
    #given
    status = Status.IN_PROGRESS

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.can_delete() == False

def test_next_status_done_state():
    #given
    status = Status.DONE

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.next_status() == Status.TODO

def test_next_status_todo_state():
    #given
    status = Status.TODO

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.next_status() == Status.IN_PROGRESS

def test_next_status_in_progress_state():
    #given
    status = Status.IN_PROGRESS

    #when
    item = Item("id", "title", status, "description", "26/09/2020" )

    #then
    assert item.next_status() == Status.DONE

def test_due_date_with_date():
    #given
    date = "26/09/2020"

    #when
    item = Item("id", "title", "Todo", "description", date )

    #then
    assert item.due_date() == "26/09/2020"

def test_due_date_without_date():
    #given
    date = None

    #when
    item = Item("id", "title", "Todo", "description", date )

    #then
    assert item.due_date() == ""

def test_from_card():
    #given
    card = { 'id': 'theId',
             'name': 'theName',
             'desc': 'theDescription',
             'due': '26/09/2020',
             'dateLastActivity': '2020-07-02T07:39:25.531Z'}
    card_list = { 'name': Status.TODO }

    #when
    item = Item.from_card(card, card_list)

    #then
    assert item.id == 'theId'
    assert item.title == 'theName'
    assert item.description == 'theDescription'
    assert item.status == Status.TODO
    assert item.due == '26/09/2020'



    