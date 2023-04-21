from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from ..common.utils import check_required_keys
from ..repositories.managers import (IngredientManager, OrderManager,
                                     SizeManager, BeverageManager)
from ..controllers.base import BaseController

class OrderState(object):

    def __init__(self, context):
        self.context = context

    



#the default state will only be used when object is intializated
class Default(OrderState):

    def do_something(self):
        print("Doing something else in StateB")

class CreateOrder(OrderState):
    order_detail =''
    order_error = ''
    name ='CreateOrder'
    manager = OrderManager
    __required_info = ('client_name', 'client_dni', 'client_address', 'client_phone', 'size_id')
    
    def calculate_order_price(self,size_price: float, ingredients: list, beverages: list):
        price = sum(ingredient.price for ingredient in ingredients)+size_price +sum(beverage.price for beverage in beverages)
        return round(price, 2)

    def create(self, order: dict):
        current_order = order.copy()
        if not check_required_keys(self.__required_info, current_order):
            return 'Invalid order payload', None
        
        if current_order.get('date'):
            current_order['date']= datetime.strptime(current_order['date'], "%Y-%m-%d %H:%M:%S.%f")

        size_id = current_order.get('size_id')
        size = SizeManager.get_by_id(size_id)

        if not size:
            return 'Invalid size for Order', None

        ingredient_ids = current_order.pop('ingredients', [])
        beverage_ids = current_order.pop('beverages', [])
        try:
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverage_ids)
            price = self.calculate_order_price(size.get('price'), ingredients,beverages)
            order_with_price = {**current_order, 'total_price': price}
            self.order_detail = self.manager.create(order_with_price, ingredients)
            self.order_error =None 
        except (SQLAlchemyError, RuntimeError) as ex:
            self.order_detail = None
            self.order_error =str(ex)



class Checkin(OrderState):
    name = "Checkin"

class Checkout(OrderState):
    name = "Checkout"
