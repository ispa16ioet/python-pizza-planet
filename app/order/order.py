
from .order_state import Default,CreateOrder

class Order(object):
    def __init__(self):
        self.state = Default(self)
        self.order_detail = 'c'
        self.order_error = 's'
    def set_state(self, state):
        self.state = state

    def create_order(self,order):
        self.state.create(order = order)
        self.order_detail =self.state.order_detail
        self.order_error =self.state.order_error
    def do_something(self):
        self.state.do_something()