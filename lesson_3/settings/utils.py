from settings.jim import pack, unpack
from settings.variables import ENCODING, LOG_FILENAME, MAX_PACKAGE_LENGTH


def get_message(client):
    """
    Утилита приема и декодирования сообщения.
    Принимает байты и выдает словарь, если принято что - то другое отдает ошибку значения
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        response = unpack(encoded_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения.
    Принимает словарь и отправляет его.
    """
    encoded_message = pack(message)
    sock.send(encoded_message)
