import sys

sys.path.insert(1, "/src/src/python")

from employee import Employee
from unittest.mock import patch


def test_email():
    emp1 = Employee("Corey", "Schafer", 50000)
    emp2 = Employee("Sue", "Smith", 60000)
    assert emp1.email == "Corey.Schafer@email.com"
    assert emp2.email == "Sue.Smith@email.com"
    emp1.first = "John"
    emp2.first = "Jane"
    assert emp1.email == "John.Schafer@email.com"
    assert emp2.email == "Jane.Smith@email.com"


def test_fullname():
    emp1 = Employee("Corey", "Schafer", 50000)
    emp2 = Employee("Sue", "Smith", 60000)
    assert emp1.fullname == "Corey Schafer"
    assert emp2.fullname == "Sue Smith"
    emp1.first = "John"
    emp2.first = "Jane"
    assert emp1.fullname == "John Schafer"
    assert emp2.fullname == "Jane Smith"


def test_apply_raise():
    emp1 = Employee("Corey", "Schafer", 50000)
    emp2 = Employee("Sue", "Smith", 60000)
    emp1.apply_raise() == 52500
    emp2.apply_raise() == 63000


def test_monthly_schedule():
    emp1 = Employee("Corey", "Schafer", 50000)
    emp2 = Employee("Sue", "Smith", 60000)
    emp1.monthly_schedule


def test_monthly_schedule():
    emp1 = Employee("Corey", "Schafer", 50000)
    emp2 = Employee("Sue", "Smith", 60000)
    with patch("employee.requests.get") as mocked_get:
        mocked_get.return_value.ok = False

        schedule = emp1.monthly_schedule("May")
        mocked_get.assert_called_with("http://company.com/Schafer/May")
        assert schedule == "Bad Response!"

        mocked_get.return_value.ok = True
        mocked_get.return_value.text = "Success"
        schedule = emp2.monthly_schedule("June")
        mocked_get.assert_called_with("http://company.com/Smith/June")
        assert schedule == "Success"
