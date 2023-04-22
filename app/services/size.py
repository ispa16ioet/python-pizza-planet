from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from ..utils.utils import entity_controller_action

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    
    return entity_controller_action(SizeController.create,request.json)


@size.route('/', methods=PUT)
def update_size():
    
    return entity_controller_action(SizeController.update,request.json)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    
    return entity_controller_action(SizeController.get_by_id,_id)


@size.route('/', methods=GET)
def get_size():
    
    return entity_controller_action(SizeController.get_all)
