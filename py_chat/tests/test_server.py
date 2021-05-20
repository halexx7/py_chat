import argparse
import os.path
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from server import createParser, get_response


class TestServerFunction(unittest.TestCase):
    def test_createParser(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(type(createParser()), type(parser))

    def testsrvresponse(self):
        self.assertEqual(get_response(True), {"response": 200})
        self.assertEqual(get_response(False), {"response": 400, "error": "Bad Request"})


if __name__ == "__main__":
    unittest.main()
