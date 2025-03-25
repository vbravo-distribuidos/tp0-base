package protocolo

import (
	"net"
)

func EnviarAgencia(conn net.Conn, agencia string) (int, error) {
	return enviarString(conn, agencia)
}
