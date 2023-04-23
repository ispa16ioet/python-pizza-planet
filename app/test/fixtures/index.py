import pytest

from ..utils.functions import get_random_price, get_random_string




@pytest.fixture
def index_uri():
    return '/'



@pytest.fixture
def test_index(client, index_uri) -> dict:
    response = client.get(index_uri)
    return response