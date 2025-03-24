package serializacion

import (
	"fmt"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
)

func TicketDesdeString(texto string) *modelo.Ticket {
	var nombre, apellido, documento, nacimiento string
	var numero int
	fmt.Sscanf(texto, "%s,%s,%s,%s,%d", &nombre, &apellido, &documento, &nacimiento, &numero)
	return modelo.NewTicket(nombre, apellido, documento, nacimiento, numero)
}
