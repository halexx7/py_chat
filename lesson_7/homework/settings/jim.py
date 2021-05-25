import json
from settings.variables import ENCODING


def pack(dict_msg):
    """Упаковка сообщения"""
    str_msg = json.dumps(dict_msg)
    return str_msg.encode(ENCODING)


def unpack(bt_str):
    """Распаквка полученного сообщения"""
    str_decoded = bt_str.decode(ENCODING)
    return json.loads(str_decoded)
