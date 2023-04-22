from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func, desc

from .models import Ingredient, Order, OrderDetail, Size, Beverage, db
from .serializers import (IngredientSerializer, BeverageSerializer, OrderSerializer,
                          SizeSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Ingredient]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients ))
        cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages ))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    

class ReportManager(BaseManager):

    @classmethod
    def get_most_common_ingredient(cls,model):
        most_common_ingredients = cls.session.query(
            Ingredient.name,
            func.count(OrderDetail.ingredient_id).label('count')
        ).join(
            OrderDetail,
            Ingredient._id == OrderDetail.ingredient_id
        ).group_by(
            Ingredient.name
        ).order_by(
            func.count(OrderDetail.ingredient_id).desc()
        ).limit(3).all()

        most_common_ingredient_list = []
        for name, count in most_common_ingredients:
            most_common_ingredient_list.append({'value_name': name,'total_value':count})
        return most_common_ingredient_list or []
    
    @classmethod
    def get_less_common_ingredient(cls,model):
        less_common_ingredients= cls.session.query(
            Ingredient.name,
            func.count(OrderDetail.ingredient_id).label('count')
        ).join(
            OrderDetail,
            Ingredient._id == OrderDetail.ingredient_id
        ).group_by(
            Ingredient.name
        ).order_by(
            func.count(OrderDetail.ingredient_id).asc()
        ).limit(3).all()
        less_common_ingredient_list = []
        for name, count in less_common_ingredients:
            less_common_ingredient_list.append({'value_name': name,'total_value':count})
        return less_common_ingredient_list or []
    
    @classmethod
    def get_months_with_more_revenue(cls,model):

        revenue_by_month = cls.session.query(
        func.strftime('%Y-%m', Order.date).label('month'),
        func.sum(Order.total_price).label('revenue')
        ).group_by('month').order_by(desc('revenue')).limit(3).all()
        months_with_more_revenue = []

        for month, revenue in revenue_by_month:
            months_with_more_revenue.append({'value_name': month,'total_value':round(revenue, 2)})
        return months_with_more_revenue or []
    
    @classmethod
    def get_worst_clients(cls,model):

        total_spent = func.sum(Order.total_price).label('total_spent')
        client_spending = cls.session.query(
            Order.client_name,
            total_spent
        ).group_by(Order.client_name).subquery()

        bottom_clients = cls.session.query(
            client_spending.c.client_name,
            client_spending.c.total_spent
        ).order_by(client_spending.c.total_spent).limit(3).all()

        worst_clients = []

        for client_name, total_spent in bottom_clients:
            worst_clients.append({'value_name': client_name,'total_value':round(total_spent, 2)})
        return worst_clients or []
    
    @classmethod
    def get_best_clients(cls,model):

        total_spent = func.sum(Order.total_price).label('total_spent')
        client_spending = cls.session.query(
            Order.client_name,
            total_spent
        ).group_by(Order.client_name).subquery()

        top_clients = cls.session.query(
            client_spending.c.client_name,
            client_spending.c.total_spent
        ).order_by(desc(client_spending.c.total_spent)).limit(3).all()

        best_clients = []

        for client_name, total_spent in top_clients:
            best_clients.append({'value_name': client_name,'total_value':round(total_spent, 2)})
        return best_clients or []
    
class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()
