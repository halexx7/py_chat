import argparse
import unittest

from src.server import createParser, get_response


class TestServerFunction(unittest.TestCase):
    def test_createParser(self):
        parser = argparse.ArgumentParser
        self.assertIsInstance(createParser(), parser)
        print("srv_1")

    def testsrvresponse(self):
        self.assertEqual(get_response(True), {"response": 200})
        self.assertEqual(get_response(False), {"response": 400, "error": "Bad Request"})
        print("srv_1")


if __name__ == "__main__":
    unittest.main()
