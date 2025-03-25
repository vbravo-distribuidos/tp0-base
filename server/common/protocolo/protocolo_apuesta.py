import socket
from typing import List
from common.utils import Bet
from common.protocolo.protocolo_base import recibir_string
from common.serializacion.serializacion_apuesta import apuestas_a_string, apuestas_desde_string
from common.protocolo.protocolo_base import enviar_string



def recibir_apuestas(socket: socket.socket) -> tuple[List[Bet], int]:
    apuestas_str = recibir_string(socket)
    return apuestas_desde_string(apuestas_str)

def enviar_apuestas(socket: socket.socket, apuestas: List[Bet]):
    texto = apuestas_a_string(apuestas)
    return enviar_string(socket, texto)

