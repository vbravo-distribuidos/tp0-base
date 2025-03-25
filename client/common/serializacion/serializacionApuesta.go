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

func ApuestaDesdeString(texto string) *modelo.Apuesta {
	campos := strings.Split(texto, DELIMITADOR_COLUMNAS)
	agencia := campos[0]
	ticket := modelo.NewTicket(campos[1], campos[2], campos[3], campos[4], campos[5])
	apuesta := modelo.NewApuesta(agencia, ticket)
	return apuesta
}

func ApuestasDesdeString(texto string) []*modelo.Apuesta {
	var apuestas []*modelo.Apuesta

	if texto == "" {
		return apuestas
	}

	for _, linea := range strings.Split(texto, DELIMITADOR_FILAS) {
		apuesta := ApuestaDesdeString(linea)
		apuestas = append(apuestas, apuesta)
	}
	return apuestas
}
