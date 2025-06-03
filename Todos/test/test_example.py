import pytest


class Student:
    def __init__(self, first_name: str, last_name: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.year = year


@pytest.fixture
def default_value():
    return Student("Ashiq", "Sohan", 4)


def test_default_student(default_value):
    assert default_value.first_name == "Ashiq", "First name must be Ashiq"
    assert default_value.last_name == "Sohan", "Last name must be Sohan"
    assert default_value.year == 4
