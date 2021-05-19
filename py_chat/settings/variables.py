# Порт по умолчанию
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = "127.0.0.1"
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длина сообщений в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = "utf-8"


# Протокол JIM основные ключи
ACTION = "message"
TIME = "time"
USER = "Dave"


# Прочие ключи используемые в протоколе
PRESENCE = "presence"
RESPONSE = "response"
ERROR = "error"
RESPONSE_DEFAULT_IP_ADDRESS = "response_default_ip_address"

LOGGER_NAME = "app." + __name__
