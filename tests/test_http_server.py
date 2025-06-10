import threading
import json
import time
import urllib.request
import unittest
from src.http_server import run


class TestHTTPServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run, kwargs={'port': 8008})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

    def test_convert(self):
        url = "http://localhost:8008/convert?amount=100&from=USD&to=EUR"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            self.assertIn("converted", data)

    def test_invalid_currency(self):
        url = "http://localhost:8008/convert?amount=100&from=XYZ&to=ABC"
        try:
            urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)

    def test_history(self):
        url = "http://localhost:8008/history"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
