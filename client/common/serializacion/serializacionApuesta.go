package serializacion

import (
	"fmt"
	"strings"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
)

func ApuestaAString(apuesta *modelo.Apuesta) string {
	texto := fmt.Sprintf(
		"%d,%s,%s,%s,%s,%d",
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
	return strings.Join(textos, "\n")
}

func ApuestaDesdeString(texto string) *modelo.Apuesta {
	var nombre, apellido, documento, nacimiento string
	var agencia, numero int
	fmt.Sscanf(texto, "%d,%s,%s,%s,%s,%d", &agencia, &nombre, &apellido, &documento, &nacimiento, &numero)
	Ticket := modelo.NewTicket(nombre, apellido, documento, nacimiento, numero)
	return modelo.NewApuesta(agencia, Ticket)
}
