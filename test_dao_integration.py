import pytest
from src.util.dao import DAO


# ---------------- MOCK COLLECTION ---------------- #

class MockCollection:
    def __init__(self, mode):
        self.mode = mode

    def insert_one(self, data):
        if self.mode == "valid":
            class Result:
                inserted_id = "123"
            return Result()

        elif self.mode == "missing_field":
            raise Exception("WriteError")

        elif self.mode == "invalid_type":
            raise Exception("WriteError")

        elif self.mode == "duplicate":
            raise Exception("WriteError")

        elif self.mode == "db_failure":
            raise Exception("Database failure")

    def find_one(self, query):
        return {"_id": "123", "email": "test@example.com"}


# ---------------- FIXTURE ---------------- #

@pytest.fixture
def dao_valid():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("valid")
    return dao


@pytest.fixture
def dao_missing():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("missing_field")
    return dao


@pytest.fixture
def dao_invalid():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("invalid_type")
    return dao


@pytest.fixture
def dao_duplicate():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("duplicate")
    return dao


@pytest.fixture
def dao_failure():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("db_failure")
    return dao

# ---------------- TESTS ---------------- #

def test_create_valid(dao_valid):
    data = {"email": "test@example.com"}
    result = dao_valid.create(data)
    assert result["_id"] == "123"


def test_missing_field(dao_missing):
    with pytest.raises(Exception):
        dao_missing.create({})


def test_invalid_type(dao_invalid):
    with pytest.raises(Exception):
        dao_invalid.create({"email": 123})


def test_duplicate(dao_duplicate):
    with pytest.raises(Exception):
        dao_duplicate.create({"email": "test@example.com"})


def test_database_failure(dao_failure):
    with pytest.raises(Exception):
        dao_failure.create({"email": "test@example.com"})