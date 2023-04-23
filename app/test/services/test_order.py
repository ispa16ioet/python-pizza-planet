import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_order_service(order):
    current_order = order.json
    pytest.assume(order.status.startswith('200'))
    pytest.assume(current_order['_id'])
    pytest.assume(current_order['client_address'])
    pytest.assume(current_order['client_name'])



def test_get_order_by_id_service(client, order, order_uri):
    current_order = order.json
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_orders_service(client,create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(order.json['_id'] in returned_orders)
    

def test_change_order_state(client,order, order_uri):
    current_order = order.json
    response = client.get(f'{order_uri}change_state/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for order in returned_order:
        assert '_state' != 'OrderRealized'