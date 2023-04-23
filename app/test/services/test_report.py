import pytest

def test_get_report_service(get_report):
    report = get_report.json
    assert all(len(d['data']) == 0 for d in report)