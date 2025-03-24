package modelo

type Ticket struct {
	Nombre     string
	Apellido   string
	Documento  string
	Nacimiento string
	Numero     int
}

func NewTicket(nombre string, apellido string, documento string, nacimiento string, numero int) *Ticket {
	apuesta := &Ticket{
		Nombre:     nombre,
		Apellido:   apellido,
		Documento:  documento,
		Nacimiento: nacimiento,
		Numero:     numero,
	}
	return apuesta
}
