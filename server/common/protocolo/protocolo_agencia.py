import socket
from common.protocolo.protocolo_base import recibir_string


def recibir_agencia(socket: socket.socket) -> int:
    return int(recibir_string(socket))
