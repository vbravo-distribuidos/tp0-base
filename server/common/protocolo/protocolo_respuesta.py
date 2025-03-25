import socket

from common.modelo.respuesta import Respuesta
from common.protocolo.protocolo_base import enviar_string
from common.serializacion.serializacion_respuesta import respuesta_a_string


def enviar_respuesta(socket: socket.socket, respuesta: Respuesta) -> int:
    respuesta_str = respuesta_a_string(respuesta)
    return enviar_string(socket, respuesta_str)