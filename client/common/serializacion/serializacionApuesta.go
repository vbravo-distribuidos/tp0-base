package serializacion

import (
	"fmt"
	"strings"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
)

func ApuestaAString(apuesta *modelo.Apuesta) string {
	texto := fmt.Sprintf(
		"%s,%s,%s,%s,%s,%s",
		apuesta.Agencia,
		apuesta.Ticket.Nombre,
		apuesta.Ticket.Apellido,
		apuesta.Ticket.Documento,
		apuesta.Ticket.Nacimiento,
		apuesta.Ticket.Numero,
	)
	return texto
}

func ApuestasAString(apuestas []*modelo.Apuesta) string {
	var textos []string
	for _, apuesta := range apuestas {
		textos = append(textos, ApuestaAString(apuesta))
	}
	return strings.Join(textos, DELIMITADOR_FILAS)
}
