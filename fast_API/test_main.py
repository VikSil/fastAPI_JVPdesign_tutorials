import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from lessons import _33_testing

client = TestClient(_33_testing.router)

# to run tests from cmd: python -m pytest test_main.py


def test_read_item():
    response = client.get('/testing_items/foo', headers={'X-token': 'coneofsilence'})
    assert response.status_code == 200
    assert response.json() == {'id': 'foo', 'title': 'Foo', 'description': 'FooFoo, the white poodle'}


def test_read_item_bad_token():
    with pytest.raises(HTTPException) as response:
        client.get('/testing_items/foo', headers={'X-token': 'wrong token'})
    assert response.value.status_code == 400
    assert response.value.detail == 'Invalid X-Token header'


def test_read_nonexistent_item():
    with pytest.raises(HTTPException) as response:
        client.get('/testing_items/baz', headers={'X-token': 'coneofsilence'})
    assert response.value.status_code == 404
    assert response.value.detail == 'Item not found'


def test_create_item():
    response = client.post(
        '/testing_items',
        headers={'X-token': 'coneofsilence'},
        json={'id': 'baz', 'title': 'Baz', 'description': 'Cat Bazillio'},
    )
    assert response.status_code == 200
    assert response.json() == {'id': 'baz', 'title': 'Baz', 'description': 'Cat Bazillio'}


def test_create_item_bad_token():
    with pytest.raises(HTTPException) as response:
        client.post(
            '/testing_items',
            headers={'X-token': 'wrong token'},
            json={'id': 'baz', 'title': 'Baz', 'description': 'Cat Bazillio'},
        )
    assert response.value.status_code == 400
    assert response.value.detail == 'Invalid X-Token header'


def test_create_existing_item():
    with pytest.raises(HTTPException) as response:
        client.post(
            '/testing_items',
            headers={'X-token': 'coneofsilence'},
            json={'id': 'foo', 'title': 'Foo', 'description': 'FooFoo, the white poodle'},
        )
    assert response.value.status_code == 400
    assert response.value.detail == 'Item already exists'
