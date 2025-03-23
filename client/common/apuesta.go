package common

type Apuesta struct {
	agencia    int
	nombre     string
	apellido   string
	documento  string
	nacimiento string
	numero     int
}

func NewApuesta(agencia int, nombre string, apellido string, documento string, nacimiento string, numero int) *Apuesta {
	apuesta := &Apuesta{
		agencia:    agencia,
		nombre:     nombre,
		apellido:   apellido,
		documento:  documento,
		nacimiento: nacimiento,
		numero:     numero,
	}
	return apuesta
}
