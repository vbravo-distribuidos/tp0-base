package serializacion

import (
	"strings"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
)

func TicketDesdeString(texto string) *modelo.Ticket {
	partes := strings.Split(texto, DELIMITADOR_COLUMNAS)
	return modelo.NewTicket(
		partes[0],
		partes[1],
		partes[2],
		partes[3],
		partes[4],
	)
}
