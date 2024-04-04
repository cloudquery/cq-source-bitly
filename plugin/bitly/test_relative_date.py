from datetime import datetime, timedelta
from .relative_date import get_date


def test_returns_exact_date():
    result = get_date("2024-01-01")
    assert result == datetime(2024, 1, 1)

def test_throws_error_on_input_without_space_thats_not_a_date():
    try:
        get_date("xday")
        assert False
    except ValueError as e:
        assert str(e) == "Invalid relative date string."

def test_throws_error_on_input_without_number_in_relative_date():
    try:
        get_date("x day")
        assert False
    except ValueError as e:
        assert str(e) == "Invalid relative date string."

def test_throws_error_on_input_without_supported_unit_in_relative_date():
    try:
        get_date("1 x")
        assert False
    except ValueError as e:
        assert str(e) == "Invalid relative date string."

def test_returns_minus_x_days():
    for i in range(1, 2):
        result = get_date(f"-{i} days")
        assert result.date() == (datetime.now() - timedelta(days=i)).date()
        result = get_date(f"-{i} day")
        assert result.date() == (datetime.now() - timedelta(days=i)).date()

def test_returns_minus_x_weeks():
    for i in range(1, 2):
        result = get_date(f"-{i} weeks")
        assert result.date() == (datetime.now() - timedelta(weeks=i)).date()
        result = get_date(f"-{i} week")
        assert result.date() == (datetime.now() - timedelta(weeks=i)).date()


