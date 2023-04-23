import pytest

def test_test_connection(test_index):
    index = test_index.json
    pytest.assume(test_index.status.startswith('200'))
    pytest.assume(index['version']=='0.0.2')  
    pytest.assume(index['status']=='up')