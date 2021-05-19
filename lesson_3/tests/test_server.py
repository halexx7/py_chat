# -*- coding: utf-8 -*-

import os.path
import sys
import unittest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import server


class TestServerFunction(unittest.TestCase):
    def testsrvresponse(self):
        self.assertEqual(server.srv_response(True), {"response": 200, "alert": "OK"})
        self.assertEqual(
            server.srv_response(False), {"response": 400, "alert": "Not OK"}
        )


if __name__ == "__main__":
    unittest.main()