import logging
import signal
import socket
from typing import List

from common.concurso import (
    almacenar_apuestas_por_agencia,
    responder_ganadores_por_agencia,
)


class Server:
    def __init__(self, port, listen_backlog, cantidad_clientes: int):
        # Initialize server socket
        self.cantidad_clientes = cantidad_clientes
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

        try:
            socket_agencias = self.aceptar_agencias(self.cantidad_clientes)
            almacenar_apuestas_por_agencia(socket_agencias, self.cantidad_clientes)
            logging.info("action: sorteo | result: success")
            responder_ganadores_por_agencia(socket_agencias, self.cantidad_clientes)
        except OSError as e:
            if self.senial_sigterm_recibida:
                logging.info(
                    "action: finalizacion | result: success | mensaje: termino por sigterm"
                )
            else:
                logging.error(f"action: finalizacion | result: fail | error: {e}")

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
