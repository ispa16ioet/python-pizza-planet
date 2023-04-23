import pytest
from app.controllers import ReportController

def test_test_get_most_common_ingredient(app,create_orders):
    
    report = ReportController.get_most_common_ingredient()
    assert ReportController.get_most_common_ingredient() !=[] 
    assert all(d['value_name']  for d in report)
    assert all(d['total_value'] for d in report)

def test_get_less_common_ingredient(app,create_orders) :

    report = ReportController.get_less_common_ingredient()
    assert ReportController.get_less_common_ingredient() !=[]
    assert all(d['value_name']  for d in report)
    assert all(d['total_value'] for d in report)

def test_get_months_with_more_revenue(app,create_orders) :

    report = ReportController.get_months_with_more_revenue()
    assert ReportController.get_months_with_more_revenue() !=[]
    assert all(d['value_name']  for d in report)
    assert all(d['total_value'] for d in report)

def test_get_best_clients(app,create_orders) :

    report = ReportController.get_best_clients()
    assert ReportController.get_best_clients() !=[]
    assert all(d['value_name']  for d in report)
    assert all(d['total_value'] for d in report)

def test_get_worst_clients(app,create_orders) :

    report = ReportController.get_worst_clients()
    assert ReportController.get_worst_clients() !=[]
    assert all(d['value_name']  for d in report)
    assert all(d['total_value'] for d in report)
    