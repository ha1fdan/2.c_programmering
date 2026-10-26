import base64

import pytest


def create(client, item):
    return client.post('/api/admin/items', json=item)


def test_pages_render(client):
    assert client.get('/').status_code == 200
    assert client.get('/admin').status_code == 200


def test_weight_is_none_until_scale_reports(client, kiosk):
    assert client.get('/api/weight').json == {'weight': None}
    kiosk.latest_weight = 541.0
    assert client.get('/api/weight').json == {'weight': 541.0}


def test_items_starts_empty(client):
    assert client.get('/api/items').json == []


def test_create_and_list(client, cola):
    res = create(client, cola)
    assert res.status_code == 201
    items = client.get('/api/items').json
    assert len(items) == 1
    assert items[0]['id'] == res.json['id']
    assert items[0]['name'] == 'Cola' and items[0]['weight_g'] == 532


def test_create_accepts_form_strings_and_blank_category(client):
    res = create(client, {'name': ' Bar ', 'price': '10', 'weight_g': '45', 'category': '', 'stock': '3'})
    assert res.status_code == 201
    item = client.get('/api/items').json[0]
    assert item['name'] == 'Bar' and item['category'] is None and item['stock'] == 3


def test_duplicate_name_conflicts(client, cola):
    create(client, cola)
    assert create(client, cola).status_code == 409


@pytest.mark.parametrize('patch', [
    {'name': ''},
    {'price': -1},
    {'weight_g': 0},
    {'tolerance_g': -1},
    {'stock': -1},
    {'price': 'abc'},
])
def test_invalid_item_is_rejected(client, cola, patch):
    res = create(client, {**cola, **patch})
    assert res.status_code == 400
    assert 'error' in res.json
    assert client.get('/api/items').json == []


def test_missing_fields_are_rejected(client):
    assert create(client, {'name': 'X'}).status_code == 400


def test_update(client, cola):
    item_id = create(client, cola).json['id']
    res = client.put(f'/api/admin/items/{item_id}', json={**cola, 'price': 20, 'stock': 3})
    assert res.status_code == 200
    item = client.get('/api/items').json[0]
    assert item['price'] == 20 and item['stock'] == 3


def test_update_unknown_item_is_404(client, cola):
    assert client.put('/api/admin/items/99', json=cola).status_code == 404


def test_update_to_taken_name_conflicts(client, cola):
    create(client, cola)
    other = create(client, {**cola, 'name': 'Fanta'}).json['id']
    assert client.put(f'/api/admin/items/{other}', json=cola).status_code == 409


def test_delete(client, cola):
    item_id = create(client, cola).json['id']
    assert client.delete(f'/api/admin/items/{item_id}').status_code == 200
    assert client.get('/api/items').json == []
    assert client.delete(f'/api/admin/items/{item_id}').status_code == 404


def test_checkout_reduces_stock_and_never_goes_negative(client, cola):
    item_id = create(client, {**cola, 'stock': 2}).json['id']
    assert client.post('/api/checkout', json={'ids': [item_id, item_id, item_id]}).json == {'ok': True}
    assert client.get('/api/items').json[0]['stock'] == 0


def test_checkout_with_empty_basket(client, cola):
    create(client, cola)
    assert client.post('/api/checkout', json={'ids': []}).status_code == 200
    assert client.get('/api/items').json[0]['stock'] == 10


class TestAdminPassword:
    @pytest.fixture(autouse=True)
    def password(self, kiosk):
        kiosk.ADMIN_PASSWORD = 'secret'

    @staticmethod
    def auth(password):
        return {'Authorization': 'Basic ' + base64.b64encode(f'admin:{password}'.encode()).decode()}

    def test_admin_requires_login(self, client, cola):
        assert client.get('/admin').status_code == 401
        assert client.get('/admin').headers['WWW-Authenticate'].startswith('Basic')
        assert create(client, cola).status_code == 401
        assert client.delete('/api/admin/items/1').status_code == 401

    def test_wrong_password_is_rejected(self, client):
        assert client.get('/admin', headers=self.auth('nope')).status_code == 401

    def test_right_password_works(self, client, cola):
        assert client.get('/admin', headers=self.auth('secret')).status_code == 200
        assert client.post('/api/admin/items', json=cola, headers=self.auth('secret')).status_code == 201

    def test_kiosk_stays_public(self, client):
        assert client.get('/').status_code == 200
        assert client.get('/api/items').status_code == 200
        assert client.get('/api/weight').status_code == 200
