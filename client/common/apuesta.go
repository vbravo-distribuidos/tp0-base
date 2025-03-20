package common

type Apuesta struct {
	nombre     string
	apellido   string
	documento  string
	nacimiento string
	numero     int
}

func NewApuesta(nombre string, apellido string, documento string, nacimiento string, numero int) *Apuesta {
	apuesta := &Apuesta{
		nombre:     nombre,
		apellido:   apellido,
		documento:  documento,
		nacimiento: nacimiento,
		numero:     numero,
	}
	return apuesta
}
