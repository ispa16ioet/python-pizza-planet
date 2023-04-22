from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..controllers import OrderController
from ..order.order import Order
from ..order.order_state import CreateOrder,OnPreparing, Sended, Finish
order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    new_order = Order()
    new_order.set_state(CreateOrder(new_order))
    new_order.create_order(request.json)
    response = new_order.order_detail if not new_order.order_error else {'error': new_order.order_error}
    status_code = 200 if not new_order.order_error else 400
    return jsonify(response), status_code


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    new_order = Order()
    new_order.get_order_by_id(_id)
    response = new_order.order_detail if not new_order.order_error else {'error': new_order.order_error}
    status_code = 200 if not new_order.order_error else 400
    
    return jsonify(response), status_code

@order.route('/change_state/<_id>', methods=GET)
def change_state(_id: int):

    new_order = Order()
    new_order.get_order_by_id(_id)
    if new_order.order_detail['state']=='OrderRealized':
        new_order.set_state(OnPreparing(new_order))
    elif new_order.order_detail['state']=='OnPreparing':
        new_order.set_state(Sended(new_order))
    elif new_order.order_detail['state']=='Sended':
        new_order.set_state(Finish(new_order))

    response = new_order.order_detail if not new_order.order_error else {'error': new_order.order_error}
    status_code = 200 if not new_order.order_error else 400
    
    
    return jsonify(response), status_code


@order.route('/', methods=GET)
def get_orders():
    new_order = Order()
    new_order.get_all_orders()
    response = new_order.order_detail if not new_order.order_error else {'error': new_order.order_error}
    status_code = 200 if not new_order.order_error else 400
    return jsonify(response), status_code
