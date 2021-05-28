from pickle import dumps, loads

def pack(dict_msg):
    """Упаковка сообщения"""
    return dumps(dict_msg)


def unpack(bt_str):
    """Распаквка полученного сообщения"""
    return loads(bt_str)
