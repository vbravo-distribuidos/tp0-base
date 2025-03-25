package modelo

type Apuesta struct {
	Agencia string
	Ticket  *Ticket
}

func NewApuesta(agencia string, Ticket *Ticket) *Apuesta {
	apuesta := &Apuesta{
		Agencia: agencia,
		Ticket:  Ticket,
	}
	return apuesta
}
