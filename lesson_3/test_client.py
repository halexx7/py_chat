import unittest
from client import send_msg, print_msg, cli_recv
import server

class TestClientFunction(unittest.TestCase):

    def testsendmsg(self):
        self.assertEqual(send_msg(
            {
                "action": "authenticate",
                "time": "<unix timestamp>",
                "user": {
                        "account_name": "Maver1ck",
                        "password": "Correct"
                }
            }
        ), False)

    def testcli_recv(self):
        self.assertEqual(cli_recv(1024), (b'\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x08response\x94K\xc8\x8c\x05alert\x94\x8c\x04\xd0\x9e\xd0\x9a\x94u.'))


    def testprint_msg(self):
        self.assertEqual(print_msg({'response': 200, 'alert': 'ОК'}), "Сообщение от сервера: {'response': 200, 'alert': 'ОК'}")
   

if __name__ == '__main__':
    unittest.main()