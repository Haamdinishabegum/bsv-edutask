import pytest
from src.controllers.usercontroller import UserController


class MockDAO:
    def __init__(self, result):
        self.result = result

    def find(self, query):
        email = query.get("email")
        return [user for user in self.result if user.email == email]


class MockUser:
    def __init__(self, email):
        self.email = email


def create_controller(mock_result):
    dao = MockDAO(mock_result)
    return UserController(dao)


def test_single_user_found():
    user = MockUser("test@example.com")
    controller = create_controller([user])

    result = controller.get_user_by_email("test@example.com")

    assert result.email == "test@example.com"


def test_multiple_users_found(capfd):
    user1 = MockUser("test@example.com")
    user2 = MockUser("test@example.com")
    controller = create_controller([user1, user2])

    result = controller.get_user_by_email("test@example.com")

    out, err = capfd.readouterr()
    assert "more than one user" in out.lower()
    assert result.email == "test@example.com"


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

    with pytest.raises(ValueError):
        controller.get_user_by_email(None)


def test_invalid_email_partial():
    controller = create_controller([])

    with pytest.raises(ValueError):
        controller.get_user_by_email("test@")