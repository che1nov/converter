import threading
import time
import requests
import pytest
from src.http_server import run


@pytest.fixture(scope="module")
def http_server():
    server_thread = threading.Thread(target=run, kwargs={"port": 8008})
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)
    yield server_thread


def test_convert(http_server):
    url = "http://localhost:8008/convert?amount=100&from=USD&to=EUR"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    assert "converted" in data


def test_invalid_currency(http_server):
    url = "http://localhost:8008/convert?amount=100&from=XYZ&to=ABC"
    response = requests.get(url)
    assert response.status_code == 400


def test_history(http_server):
    url = "http://localhost:8008/history"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    assert isinstance(data, list)
