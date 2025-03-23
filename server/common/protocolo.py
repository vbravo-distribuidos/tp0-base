import socket

from common.respuesta import Respuesta
from common.serializacion import apuesta_desde_string, respuesta_a_string
from common.utils import Bet

TAMANIO_UINT32 = 4
TAMANIO_BUFFER = 1024
ORDEN_BYTES = "big"
CODIFICACION = "utf-8"


def recibir_bytes(socket: socket.socket, cantidad_bytes: int) -> bytearray:
    bytes_recibidos = bytearray()
    while len(bytes_recibidos) < cantidad_bytes:
        bytes_recibido = socket.recv(
            min(cantidad_bytes - len(bytes_recibidos), TAMANIO_BUFFER)
        )
        bytes_recibidos.extend(bytes_recibido)
    return bytes_recibidos


def recibir_uint32(socket: socket.socket) -> int:
    bytes_recibidos = recibir_bytes(socket, TAMANIO_UINT32)
    return int.from_bytes(bytes_recibidos, byteorder=ORDEN_BYTES)


def recibir_string(socket: socket.socket) -> str:
    longitud = recibir_uint32(socket)
    bytes_recibidos = recibir_bytes(socket, longitud)
    return bytes_recibidos.decode(CODIFICACION)


def recibir_apuesta(socket: socket.socket) -> Bet:
    apuesta_str = recibir_string(socket)
    return apuesta_desde_string(apuesta_str)


def enviar_bytes(socket: socket.socket, datos: bytes) -> int:
    cantidad_enviada = 0
    while cantidad_enviada < len(datos):
        cantidad_enviada += socket.send(datos[cantidad_enviada:])
    return cantidad_enviada


def enviar_uint32(socket: socket.socket, numero: int) -> int:
    return enviar_bytes(socket, numero.to_bytes(TAMANIO_UINT32, byteorder=ORDEN_BYTES))


def enviar_string(socket: socket.socket, mensaje: str) -> int:
    mensaje_codificado = mensaje.encode(CODIFICACION)
    enviar_uint32(socket, len(mensaje_codificado))
    return enviar_bytes(socket, mensaje_codificado)


def enviar_respuesta(socket: socket.socket, respuesta: Respuesta) -> int:
    respuesta_str = respuesta_a_string(respuesta)
    return enviar_string(socket, respuesta_str)
