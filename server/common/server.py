import logging
import signal
import socket

from common.protocolo import enviar_respuesta, recibir_apuesta
from common.respuesta import Respuesta
from common.utils import store_bets


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self.esta_corriendo = True
        signal.signal(signal.SIGTERM, self.salir_elegantemente)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)

    def salir_elegantemente(self, signum, frame):
        self.esta_corriendo = False
        logging.info("action: signal_received | result: success")

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server
        while self.esta_corriendo:
            client_sock = self.__accept_new_connection()
            self.__handle_client_connection(client_sock)

        self._server_socket.close()

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            # TODO: Modify the receive to avoid short-reads
            apuesta = recibir_apuesta(client_sock)
            store_bets([apuesta])
            logging.info(
                f"action: apuesta_almacenada | result: success | dni: {apuesta.document} | numero: {apuesta.number}"
            )
            respuesta = Respuesta("OK")
            enviar_respuesta(client_sock, respuesta)
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

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
