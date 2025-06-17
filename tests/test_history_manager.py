import os
import json
import pytest
from history_manager import HistoryManager


@pytest.fixture
def history_manager(tmp_path):
    """Provides a HistoryManager instance with a temporary file."""
    file_path = tmp_path / "test_operations.json"
    manager = HistoryManager(file_path=str(file_path))
    yield manager


def test_add_and_get_operations(history_manager):
    operation = {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR",
        "converted_amount": 92.0,
    }
    history_manager.add_operation(operation)
    assert history_manager.get_operations() == [operation]


def test_empty_history(history_manager):
    assert history_manager.get_operations() == []


def test_save_operations(history_manager):
    operation = {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR",
        "converted_amount": 92.0,
    }
    history_manager.add_operation(operation)

    file_path = history_manager.file_path
    assert os.path.exists(file_path)
    with open(file_path, "r") as file:
        data = json.load(file)
        assert data == [operation]
