import socket
from typing import List
from common.utils import Bet
from common.protocolo.protocolo_base import recibir_string
from common.serializacion.serializacion_apuesta import apuestas_desde_string


def recibir_apuestas(socket: socket.socket) -> List[Bet]:
    apuestas_str = recibir_string(socket)
    return apuestas_desde_string(apuestas_str)
