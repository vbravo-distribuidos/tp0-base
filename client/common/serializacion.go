package common

import "fmt"

func apuestaAString(apuesta *Apuesta) string {
	texto := fmt.Sprintf(
		"%s,%s,%s,%s,%d",
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
	var numero int
	fmt.Sscanf(texto, "%s,%s,%s,%s,%d", &nombre, &apellido, &documento, &nacimiento, &numero)
	return NewApuesta(nombre, apellido, documento, nacimiento, numero)
}
