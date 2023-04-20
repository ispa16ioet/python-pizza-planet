from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    
    most_common_ingredients = ReportController.get_most_common_ingredient()
    less_common_ingredient = ReportController.get_less_common_ingredient()
    months_with_more_revenue = ReportController.get_months_with_more_revenue()
    best_clients = ReportController.get_best_clients()
    worst_clients = ReportController.get_worst_clients()
    

    report = [{'report_name':'Most Common Ingredients','report_id':'most_common_ingredients','description':' most common ingredients used in the current year','data':most_common_ingredients,'symbol':''
              },{'report_name':'Less Common Ingredient','report_id':'less_common_ingredient','description':' less common ingredients used in the current year','data':less_common_ingredient,'symbol':''
              },{'report_name':'Months With More Revenue','report_id':'months_with_more_revenue','description':' months with more revenue in the current year','data':months_with_more_revenue,'symbol':'$'
              },{'report_name':'Best Clients','report_id':'best_clients','description':' clients that had waste the most in the current year','data':best_clients,'symbol':'$'
              },{'report_name':'Worst Clients','report_id':'worst_clients','description':' clients that had waste the less in the current year','data':worst_clients,'symbol':'$'
              }   
              ]
    status_code = 200 if report else 400 
    return jsonify(report), status_code
