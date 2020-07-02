import os
import requests
from item import Item

"""
A Global to be used to cache the doard ID
"""
BOARD_ID = ""


def build_url(endpoint):
    """
    Builds the API url from a base URL and the specific endpoint for Trello.

    Args:
        endpoint: The endpoint to be called.

    Returns:
        url: The full url for the endpoint.
    """
    return os.getenv('TRELLO_BASE_URL') + endpoint


def get_default_params():
    """
    Gets the default parameter to be added to all calls to Trello. Specifically the key 
    and the token

    Returns:
        params: A map with the default parameters.
    """
    return {
        'key': os.getenv('TRELLO_KEY'),
        'token': os.getenv('TRELLO_TOKEN')
    }


def get_boards():
    """
    Gets all the boards for the currnt user

    Returns:
        boards: json object containing the baords.
    """
    params = get_default_params()
    url = build_url('/members/me/boards')

    response = requests.get(url, params=params)
    boards = response.json()

    return boards


def get_board_id():
    """
    Gets the board ID which is to be used for this application from Trello id not already cached

    Returns:
        id: The board ID.
    """
    global BOARD_ID
    if BOARD_ID == "":
        boards = get_boards()
        BOARD_ID = next(
            (board['id'] for board in boards if board['name'] == "ToDoBoard"), None)
    return BOARD_ID


def get_lists(include_cards=True):
    """
    Fetches all lists from the board in Trello.

    Args:
        include_cards: A flag to indicate is the items in the list should also be returned.

    Returns:
        list: The list of saved items.
    """
    board_id = get_board_id()

    params = get_default_params()
    if include_cards:
        params.update({'cards': 'all'})
    url = build_url('/boards/%s/lists' % board_id)

    response = requests.get(url, params=params)
    lists = response.json()

    return lists


def get_list(name):
    """
    Fetches the list with the sepcific name.

    Args:
        name: The name of the list to return.

    Returns:
        item: The list of items, or None if no list match the specified name.
    """
    lists = get_lists(False)
    return next((list for list in lists if list['name'] == name), None)


def get_items():
    """
    Fetches all saved items from the Trello.

    Returns:
        list: The list of saved items.
    """
    card_lists = get_lists()

    items = []
    for card_list in card_lists:
        for card in card_list['cards']:
            items.append(
                Item(card['id'],
                     card['name'],
                     card_list['name'],
                     card['desc'],
                     card['due']))

    items = sorted(items, key=lambda kv: kv.id)
    items = sorted(items, key=lambda kv: kv.status, reverse=True)

    return items


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title, description, due):
    """
    Adds a new item with the specified title to the Trello.

    Args:
        title: The title of the item.
        description:
        due:

    Returns:
        item: The new saved item.
    """
    todo_list = get_list('ToDo')

    params = get_default_params()
    params.update({
        'name': title, 
        'idList': todo_list['id'], 
        'desc': description, 
        'due': due})
    url = build_url('/cards')

    response = requests.post(url, params=params)
    item = response.json()

    return item


def update_item(id, next_status):
    """
    Update the status of an existing item in the Trello.

    Args:
        id: The id of the item to updated.

    Returns:
        item: The updated item.
    """
    new_list = get_list(next_status)

    params = get_default_params()
    params.update({'idList': new_list['id']})
    url = build_url('/cards/%s' % id)

    response = requests.put(url, params=params)
    item = response.json()

    return item


def remove_item(id):
    """
    Removes an existing item in the Trello.

    Args:
        id: The id of the item to remove.

    Returns:
        response: from the api call.
    """
    params = get_default_params()
    url = build_url('/cards/%s' % id)

    response = requests.delete(url, params=params)
    return response
