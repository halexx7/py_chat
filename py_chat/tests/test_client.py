import os.path
import socket
import sys
import unittest
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from client import presets_msg, createParser
from settings.utils import get_message, send_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, RESPONSE


class TestClientFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.transport = socket.socket()
        return super().setUp()


    def test_createParser(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(type(createParser()), type(parser))


    def test_process_ans(self):
        server_address, server_port = DEFAULT_IP_ADDRESS, DEFAULT_PORT
        self.transport.connect((server_address, server_port))
        self.message_to_server = presets_msg()
        send_message(self.transport, self.message_to_server)
        self.answer = get_message(self.transport)
        self.assertEqual(self.answer[RESPONSE], 200)
        self.transport.close()


if __name__ == "__main__":
    unittest.main()
