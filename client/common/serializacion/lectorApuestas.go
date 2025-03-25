package serializacion

import (
	"bufio"
	"os"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/modelo"
)

type LectorApuestas struct {
	archivo        *os.File
	scanner        *bufio.Scanner
	agencia        string
	cantidadMaxima int
}

func NewLectorApuestas(ruta string, agencia string, cantidadMaxima int) (*LectorApuestas, error) {
	file, err := os.Open(ruta)
	if err != nil {
		return nil, err
	}

	scanner := bufio.NewScanner(file)
	lector := &LectorApuestas{archivo: file, scanner: scanner, agencia: agencia, cantidadMaxima: cantidadMaxima}
	return lector, nil
}

func (l *LectorApuestas) Leer() []*modelo.Apuesta {
	var apuestas []*modelo.Apuesta
	i := 0
	for i < l.cantidadMaxima && l.scanner.Scan() {
		linea := l.scanner.Text()
		ticket := TicketDesdeString(linea)
		apuesta := modelo.NewApuesta(l.agencia, ticket)
		apuestas = append(apuestas, apuesta)
		i++
	}
	return apuestas
}

func (l *LectorApuestas) Cerrar() error {
	return l.archivo.Close()
}
