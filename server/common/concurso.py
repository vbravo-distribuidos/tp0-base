import logging
import socket
from multiprocessing import Manager, Pool
from typing import List

from common.modelo.respuesta import Respuesta
from common.protocolo.protocolo_agencia import recibir_agencia
from common.protocolo.protocolo_apuesta import enviar_apuestas, recibir_apuestas
from common.protocolo.protocolo_respuesta import enviar_respuesta
from common.utils import Bet, has_won, load_bets, store_bets


def almacenar_apuestas_por_agencia(
    socket_agencias: List[socket.socket], lock, pool):
    tareas = [(socket, lock) for socket in socket_agencias]
    pool.map(func=almacenar_apuestas, iterable=tareas)


def almacenar_apuestas(args):
    client_sock, lock = args

    while True:
        apuestas, cantidad_errores = recibir_apuestas(client_sock)
        if len(apuestas) == 0:
            logging.info(
                "action: apuesta_vacia | result: success | mensaje: termina procesamiento de batches"
            )
            break

        with lock:
            store_bets(apuestas)

        if cantidad_errores == 0:
            respuesta = Respuesta("OK")
            logging.info(
                f"action: apuesta_recibida | result: success | cantidad: {len(apuestas)}"
            )
        else:
            respuesta = Respuesta("ERROR")
            logging.warning(
                f"action: apuesta_recibida | result: fail | cantidad: {len(apuestas)}"
            )
        enviar_respuesta(client_sock, respuesta)

    logging.info("action: saliendo del while | result: success")


def filtrar_ganadores(agencia: int, apuestas: List[Bet]) -> List[Bet]:
    return [
        apuesta
        for apuesta in apuestas
        if apuesta.agency == agencia and has_won(apuesta)
    ]


def responder_ganadores_por_agencia(
    socket_agencias: List[socket.socket], pool
):
    pool.map(func=responder_ganadores, iterable=socket_agencias)


def responder_ganadores(socket: socket.socket):
    apuestas = load_bets()
    agencia = recibir_agencia(socket)
    logging.info(f"action: recibir_agencias | result: success | agencia: {agencia}")
    ganadores = filtrar_ganadores(agencia, apuestas)
    enviar_apuestas(socket, ganadores)
    logging.info(
        f"action: apuestas_enviadas | result: success | apuestas: {len(ganadores)}"
    )


def cerrar_conexiones(sockets: List[socket.socket]):
    for socket in sockets:
        socket.close()
    logging.info("action: cerrar_conexion | result: success")
