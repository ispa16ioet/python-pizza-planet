from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..order.order import Order
from ..order.order_state import CreateOrder
from ..utils.utils import change_order_state,state_controll_action

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(request.json)
    
    return state_controll_action(new_order)

@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    new_order = Order()
    new_order.get_order_by_id(_id)
    return state_controll_action(new_order)

@order.route('/change_state/<_id>', methods=GET)
def change_state(_id: int):

    new_order = Order()
    new_order.get_order_by_id(_id)
    change_order_state(new_order)

    return state_controll_action(new_order)


@order.route('/', methods=GET)
def get_orders():
    new_order = Order()
    new_order.get_all_orders()

    return state_controll_action(new_order)
