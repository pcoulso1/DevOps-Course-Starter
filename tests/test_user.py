import pytest

from user.user import User
from user.user_role import UserRole

def test_role_reader():
    #given
    role = UserRole.READER

    #when
    user = User("fred", 1234, "login", "fred@email.com", role )

    #then
    assert user.is_readonly == True
    assert user.is_admin == False

def test_role_writer():
    #given
    role = UserRole.WRITER

    #when
    user = User("fred", 1234, "login", "fred@email.com", role )

    #then
    assert user.is_readonly == False
    assert user.is_admin == False

def test_role_admin():
    #given
    role = UserRole.ADMIN

    #when
    user = User("fred", 1234, "login", "fred@email.com", role )

    #then
    assert user.is_readonly == False
    assert user.is_admin == True

def test_from_json():
    #given
    json = { 'id': 1234,
             'name': 'theName',
             'login': 'thelogin',
             'email': 'theEmail',
             'role': UserRole.ADMIN,
             'updated': '2020-07-02T07:39:25.531Z' }

    #when
    user = User.from_json(json)

    #then
    assert user.id == 1234
    assert user.name == 'theName'
    assert user.login == 'thelogin'
    assert user.email == 'theEmail'
    assert user.role == UserRole.ADMIN
    assert user.updated == '2020-07-02T07:39:25.531Z'

def test_from_json_no_role_updated():
    #given
    json = { 'id': 1234,
             'name': 'theName',
             'login': 'thelogin',
             'email': 'theEmail' }

    #when
    user = User.from_json(json)

    #then
    assert user.id == 1234
    assert user.name == 'theName'
    assert user.login == 'thelogin'
    assert user.email == 'theEmail'
    assert user.role == UserRole.READER
    assert user.updated is None
    