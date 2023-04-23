import pytest
import json
from flask import Response

from app.controllers import (IngredientController,
                             SizeController)
from app.controllers.base import BaseController
from app.test.utils.functions import get_random_choice, shuffle_list
from app.order.order import Order
from app.order.order_state import CreateOrder
from app.utils.utils import change_order_state,state_controll_action

def __order(ingredients: list, size: dict, client_data: dict):
    ingredients = [ingredient.get('_id') for ingredient in ingredients]
    size_id = size.get('_id')
    return {
        **client_data,
        'ingredients': ingredients,
        'size_id': size_id
    }


def __create_items(items: list, controller: BaseController):
    created_items = []
    for ingredient in items:
        created_item, _ = controller.create(ingredient)
        created_items.append(created_item)
    return created_items


def __create_sizes_and_ingredients(ingredients: list, sizes: list):
    created_ingredients = __create_items(ingredients, IngredientController)
    created_sizes = __create_items(sizes, SizeController)
    return created_sizes if len(created_sizes) > 1 else created_sizes.pop(), created_ingredients


def test_create(app, ingredients, size, client_data):
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(order)
    created_order, status_code = state_controll_action(new_order)
    
    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])
    
    json_data = created_order.get_data()
    json_string = json_data.decode('utf-8')
    created_order = json.loads(json_string)

    pytest.assume(status_code is 200)
    
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order['_id'])
        pytest.assume(size_id == created_order['size']['_id'])

        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test_calculate_order_price(app, ingredients, size, client_data):
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(order)
    created_order, _ = state_controll_action(new_order)
    
    json_data = created_order.get_data()
    json_string = json_data.decode('utf-8')
    created_order = json.loads(json_string)

    pytest.assume(created_order['total_price'] == round(created_size['price'] + sum(ingredient['price'] for ingredient in created_ingredients), 2))


def test_get_by_id(app, ingredients, size, client_data):
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    #create order
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(order)
    created_order =  new_order.order_detail

    #get order
    search_order = Order()
    search_order.get_order_by_id(new_order.order_detail['_id'])
    order_from_db, error = search_order.order_detail, search_order.order_error

    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])


    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order['size']['_id'])

        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test_get_all(app, ingredients, sizes, client_data):
    created_sizes, created_ingredients = __create_sizes_and_ingredients(ingredients, sizes)
    created_orders = []
    for _ in range(5):
        order = __order(shuffle_list(created_ingredients)[:3], get_random_choice(created_sizes), client_data)
        new_order = Order()
        new_order.set_state(CreateOrder(new_order))
        new_order.create_order(order)
        created_order =  new_order.order_detail
        created_orders.append(created_order)

    new_order = Order()
    new_order.get_all_orders()
    orders_from_db, error = new_order.order_detail, new_order.order_error
    searchable_orders = {db_order['_id']: db_order for db_order in orders_from_db}
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order['_id']
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)


def test_change_states(app, ingredients, size, client_data):
    created_size, created_ingredients = __create_sizes_and_ingredients(ingredients, [size])
    order = __order(created_ingredients, created_size, client_data)
    
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(order)

    search_order = Order()
    search_order.get_order_by_id(new_order.order_detail['_id'])
    order_from_db_detail = search_order.order_detail['state']

    #iterate and change over all states
    for i in range(1,4):
        change_order_state(search_order)
    order_state_changed =search_order.order_detail

    pytest.assume(order_from_db_detail is not order_state_changed['state'])
    
