package serializacion

import "github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"

func RespuestaDesdeString(texto string) *modelo.Respuesta {
	return modelo.NewRespuesta(texto)
}
