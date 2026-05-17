import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

@pytest.fixture
def mock_setup():
    mock_dao = MagicMock()
    controller = UserController(mock_dao)
    return mock_dao, controller

@pytest.mark.unit
def test_single_user_returns_that_user(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = [{"email": "abc@def.com"}]
    result = controller.get_user_by_email("abc@def.com")
    assert result["email"] == "abc@def.com"

@pytest.mark.unit
def test_multiple_users_returns_first(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = [
        {"email": "abc@def.com", "name": "abc"},
        {"email": "abc@def.com", "name": "acb"}]
    result = controller.get_user_by_email("abc@def.com")
    assert result["email"] == "abc@def.com" and result["name"] == "abc"

@pytest.mark.unit
def test_no_user_found_returns_none(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.return_value = []
    result = controller.get_user_by_email("abc@def.com")
    assert result is None

@pytest.mark.unit
def test_invalid_email_raises_value_error(mock_setup):
    _, controller = mock_setup
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid email")

@pytest.mark.unit
def test_dao_exception(mock_setup):
    mock_dao, controller = mock_setup
    mock_dao.find.side_effect = Exception("Database Problem")
    with pytest.raises(Exception):
        controller.get_user_by_email("abc@def.com")