from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    is_database_up, error = ReportController.test_connection()
    return jsonify({'version': '0.0.2', 'status': 'up' if is_database_up else 'down', 'error': error})