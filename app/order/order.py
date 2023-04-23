
from .order_state import Default

class Order(object):
    def __init__(self,OrderState = Default):
        self.state = OrderState(self)
        self.order_detail = ''
        self.order_error = None
        self.order_id = ''
    
    def set_state(self, state):
        self.state = state

    def create_order(self,order):
        self.state.create(order = order)
        self.order_detail =self.state.order_detail
        self.order_error =self.state.order_error

    def get_all_orders(self):
        self.state.get_all_orders()
        self.order_detail =self.state.order_detail
        self.order_error =self.state.order_error
    
    def get_order_by_id(self, _id):
        self.state.get_order_by_id(_id)
        self.order_detail =self.state.order_detail
        self.order_error =self.state.order_error