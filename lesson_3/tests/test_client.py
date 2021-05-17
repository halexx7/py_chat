# -*- coding: utf-8 -*-

import unittest
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import client 


class TestClientFunction(unittest.TestCase):
    def testpresersmsg(self):
        self.assertEqual(
            (client.presets_msg()),
            b"\x80\x04\x95l\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x06action\x94\x8c\x0cauthenticate\x94\x8c\x04time\x94\x8c\x10<unix timestamp>\x94\x8c\x04user\x94}\x94(\x8c\x0caccount_name\x94\x8c\x04Dave\x94\x8c\x08password\x94\x8c\x06Secret\x94uu.",
        )

    def testclirecv(self):
        msg = b"\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x08response\x94K\xc8\x8c\x05alert\x94\x8c\x04\xd0\x9e\xd0\x9a\x94u."
        self.assertEqual((client.loads_srv_msg(msg)), {"response": 200, "alert": "ОК"})


if __name__ == "__main__":
    unittest.main()
