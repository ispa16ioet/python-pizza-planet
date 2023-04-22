from app.common.http_methods import GET
from flask import Blueprint

from ..utils.utils import generate_report


report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    
    return generate_report()
