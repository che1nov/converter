import pytest
from history_manager import HistoryManager
from mongomock import MongoClient as MockMongoClient


@pytest.fixture
def history_manager():
    mock_client = MockMongoClient()
    manager = HistoryManager(mongo_client=mock_client)
    manager.collection.delete_many({})
    yield manager
    mock_client.drop_database("currency_converter")


def test_add_and_get_operations(history_manager):
    operation = {
        "amount": 100,
        "from": "USD",
        "to": "EUR",
        "converted": 92.0,
    }
    history_manager.add_operation(operation)
    del operation["_id"]
    operations = history_manager.get_operations()
    for op in operations:
        if "_id" in op:
            del op["_id"]
    assert operations == [operation]


def test_empty_history(history_manager):
    assert history_manager.get_operations() == []
