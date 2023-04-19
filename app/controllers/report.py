from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import ReportManager
from ..repositories.models import Ingredient

class ReportController:

    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        try:
            ReportManager.test_connection(model =Ingredient)
            return True, ''
        except (SQLAlchemyError, RuntimeError) as ex:
            return False, str(ex)
