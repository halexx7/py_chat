import unittest

from server import srv_response, srv_send


class TestServerFunction(unittest.TestCase):
    def testsrvresponse(self):
        self.assertEqual(srv_response(True), {"response": 200, "alert": "ОК"})
        self.assertEqual(
            srv_response(False), {"response": 400, "alert": "Not ОК"}
        )


if __name__ == "__main__":
    unittest.main()
