#action - PROBE
def action_probe():
    """Формирует и возвращает сообщение PROBE"""
    msg = {
        "action": "probe",
        "time": "<unix timestamp>"
    }
    return msg


# action - MSG
def action_msg(message, to="#all"):
    """Функция формирует сообщение MSG"""
    msg = {
        "action": "msg", 
        "time": "<unix timestamp>", 
        "to": to, 
        "from": "srv", 
        "message": message
    }
    return msg