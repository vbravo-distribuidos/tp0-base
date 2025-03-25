import logging
import signal
import socket

from common.modelo.respuesta import Respuesta
from common.utils import store_bets
from common.protocolo.protocolo_apuesta import recibir_apuestas
from common.protocolo.protocolo_respuesta import enviar_respuesta


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
        try:
            while True:
                client_sock = self.__accept_new_connection()
                self.__handle_client_connection(client_sock)
        except OSError as e:
            if self.senial_sigterm_recibida:
                logging.info("action: exit | result: success | exit by sigterm")
            else:
                logging.error(f"action: exit | result: fail | error: {e}")

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """

        try:
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
                respuesta = Respuesta("OK")
                enviar_respuesta(client_sock, respuesta)
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()
        logging.info("action: close_connection | result: success")

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
