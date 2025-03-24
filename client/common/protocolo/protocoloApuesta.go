package protocolo

import (
	"net"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/serializacion"
)

func EnviarApuestas(conn net.Conn, apuesta []*modelo.Apuesta) (int, error) {
	texto := serializacion.ApuestasAString(apuesta)
	return enviarString(conn, texto)
}
