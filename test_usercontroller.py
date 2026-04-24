import pytest
from src.controllers.usercontroller import UserController
class MockDAO:
    def __init__(self, result):
        self.result = result

    def find(self, query):
        return self.result


class MockUser:
    def __init__(self, email):
        self.email = email


def create_controller(mock_result):
    dao = MockDAO(mock_result)
    controller = UserController(dao)  # ✅ pass DAO here
    return controller



def test_single_user_found():
    user = MockUser("test@example.com")
    controller = create_controller([user])

    result = controller.get_user_by_email("test@example.com")

    assert result == user


def test_multiple_users_found():
    user1 = MockUser("test@example.com")
    user2 = MockUser("test@example.com")
    controller = create_controller([user1, user2])

    result = controller.get_user_by_email("test@example.com")

    assert result == user1  # should return first user


def test_no_user_found():
    controller = create_controller([])

    with pytest.raises(IndexError):
        controller.get_user_by_email("test@example.com")



def test_invalid_email():
    controller = create_controller([])

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")



def test_empty_email():
    controller = create_controller([])

    with pytest.raises(ValueError):
        controller.get_user_by_email("")



def test_none_email():
    controller = create_controller([])

    with pytest.raises(TypeError):
        controller.get_user_by_email(None)