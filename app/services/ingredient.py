from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from ..utils.utils import entity_controller_action

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    
    return entity_controller_action(IngredientController.create,request.json)


@ingredient.route('/', methods=PUT)
def update_ingredient():
    
    return entity_controller_action(IngredientController.update,request.json)

@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    
    return entity_controller_action(IngredientController.get_by_id,_id)


@ingredient.route('/', methods=GET)
def get_ingredients():
    
    return entity_controller_action(IngredientController.get_all)