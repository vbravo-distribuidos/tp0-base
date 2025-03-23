package common

import "fmt"

func apuestaAString(apuesta *Apuesta) string {
	texto := fmt.Sprintf(
		"%d,%s,%s,%s,%s,%d",
		apuesta.agencia,
		apuesta.nombre,
		apuesta.apellido,
		apuesta.documento,
		apuesta.nacimiento,
		apuesta.numero,
	)
	return texto
}

func apuestaDesdeString(texto string) *Apuesta {
	var nombre, apellido, documento, nacimiento string
	var agencia, numero int
	fmt.Sscanf(texto, "%d,%s,%s,%s,%s,%d", &agencia, &nombre, &apellido, &documento, &nacimiento, &numero)
	return NewApuesta(agencia, nombre, apellido, documento, nacimiento, numero)
}

func respuestaDesdeString(texto string) *Respuesta {
	return NewRespuesta(texto)
}
