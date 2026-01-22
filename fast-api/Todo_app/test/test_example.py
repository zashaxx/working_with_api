from os import major
import pytest


def test_equal_or_not_equal():
    assert 3 == 3


def test_is_instance():
    assert isinstance("hello", str)
    assert not isinstance(5, str)


def test_boolean():
    validated = True
    assert validated is True
    assert not (validated is False)
    assert ("hello" == "world") is False


def test_type():
    assert type(5) is int
    assert type("test") is str
    assert type("test") is not int


def test_greater_or_less():
    assert 10 < 14
    assert 5 > 2
    assert 7 >= 7


def test_list():
    list_a = [1, 2, 3, 4, 5]
    list_b = [False, False]
    assert 5 in list_a
    assert 10 not in list_a
    assert all(list_a)
    assert not any(list_b)


class Student:
    def __init__(self, first_name: str, last_name: str, age: int, major: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.major = major


@pytest.fixture
def default_student():
    return Student("John", "Doe", 20, "Mathematics")


def test_person_initialization(default_student):

    # x = Student("Ram", "Dahal", 23, "Computer Science")

    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Mathematics", "Major should be Mathematics "
    assert default_student.age == 20, "Age should be 20"
