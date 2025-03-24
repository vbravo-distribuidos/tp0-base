package modelo

type Apuesta struct {
	Agencia int
	Ticket  *Ticket
}

func NewApuesta(agencia int, Ticket *Ticket) *Apuesta {
	apuesta := &Apuesta{
		Agencia: agencia,
		Ticket:  Ticket,
	}
	return apuesta
}
