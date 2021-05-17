#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .lesson_3.server import srv_response

class TestServerFunction(unittest.TestCase):
    def testsrvresponse(self):
        self.assertEqual(srv_response(True), {"response": 200, "alert": "OK"})
        self.assertEqual(
            srv_response(False), {"response": 400, "alert": "Not ОК"}
        )


if __name__ == "__main__":
    unittest.main()