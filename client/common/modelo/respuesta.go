package modelo

type Respuesta struct {
	Estado string
}

func NewRespuesta(estado string) *Respuesta {
	respuesta := &Respuesta{
		Estado: estado,
	}
	return respuesta
}

func (r *Respuesta) EsOk() bool {
	return r.Estado == "OK"
}
