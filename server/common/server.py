import logging
import signal
import socket
from typing import Dict, List, Set

from common.modelo.respuesta import Respuesta
from common.utils import Bet, has_won, load_bets, store_bets
from common.protocolo.protocolo_apuesta import enviar_apuestas, recibir_apuestas
from common.protocolo.protocolo_respuesta import enviar_respuesta
from common.protocolo.protocolo_agencia import recibir_agencia
from common.serializacion.serializacion_apuesta import apuestas_a_string


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self.senial_sigterm_recibida = False
        signal.signal(signal.SIGTERM, self.salir_elegantemente)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)

    def salir_elegantemente(self, signum, frame):
        self.senial_sigterm_recibida = True
        self._server_socket.close()
        logging.info("action: signal_received | result: success")

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        cantidad_agencias = 5

        try:
            socket_agencias = self.aceptar_agencias(cantidad_agencias)
            self.almacenar_apuestas_agencias(socket_agencias)
            self.declarar_ganadores(socket_agencias)
        except OSError as e:
            if self.senial_sigterm_recibida:
                logging.info("action: finish | result: success | finish by sigterm")
            else:
                logging.error(f"action: finish | result: fail | error: {e}")

    def almacenar_apuestas_agencias(self, socket_agencias: List[socket.socket]):
        for socket_agencia in socket_agencias:
            self.almacenar_apuestas(socket_agencia)

    def almacenar_apuestas(self, client_sock: socket.socket):
        while True:
            apuestas, cantidad_errores = recibir_apuestas(client_sock)
            if len(apuestas) == 0:
                logging.info("action: bet length is zero | result: success")
                break

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

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("action: accept_connections | result: in_progress")
        c, addr = self._server_socket.accept()
        logging.info(f"action: accept_connections | result: success | ip: {addr[0]}")
        return c

    def aceptar_agencias(self, cantidad_agencias: int) -> List[socket.socket]:
        socket_agencias = []
        for _ in range(cantidad_agencias):
            client_sock = self.__accept_new_connection()
            socket_agencias.append(client_sock)
        return socket_agencias

    def filtrar_ganadores(self, agencia: int, apuestas: List[Bet]) -> List[Bet]:
        return [
            apuesta
            for apuesta in apuestas
            if apuesta.agency == agencia and has_won(apuesta)
        ]

    def declarar_ganadores(self, socket_agencias: List[socket.socket]):
        for socket in socket_agencias:
            apuestas = load_bets()
            agencia = recibir_agencia(socket)
            logging.info(
                f"action: recibir_agencias | result: success | agencia: {agencia}"
            )
            ganadores = self.filtrar_ganadores(agencia, apuestas)
            logging.info(f"action: ganadores | result: success | ganadoras: {apuestas_a_string(ganadores)}")
            enviar_apuestas(socket, ganadores)
            logging.info(
                f"action: apuestas_enviadas | result: success | apuestas: {len(ganadores)}"
            )
