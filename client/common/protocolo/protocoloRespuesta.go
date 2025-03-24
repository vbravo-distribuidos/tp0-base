package protocolo

import (
	"net"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/serializacion"
)

func RecibirRespuesta(conn net.Conn) (*modelo.Respuesta, error) {
	texto, err := recibirString(conn)
	if err != nil {
		return nil, err
	}

	return serializacion.RespuestaDesdeString(texto), nil
}
