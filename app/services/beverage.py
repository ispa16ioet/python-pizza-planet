from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request, jsonify

from ..controllers import BeverageController
from ..utils.utils import entity_controller_action

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
def create_beverage():
    
    return entity_controller_action(BeverageController.create,request.json)


@beverage.route('/', methods=PUT)
def update_beverage():

    return entity_controller_action(BeverageController.update,request.json)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    
    return entity_controller_action(BeverageController.get_by_id,_id)

@beverage.route('/', methods=GET)
def get_beverages():
    
    return entity_controller_action(BeverageController.get_all)
