import os.path
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import server


class TestServerFunction(unittest.TestCase):
    def testsrvresponse(self):
        self.assertEqual(server.get_response(True), {"response": 200})
        self.assertEqual(server.get_response(False), {"response": 400, "error": "Bad Request"})


if __name__ == "__main__":
    unittest.main()
