package common

type Respuesta struct {
	estado string
}

func NewRespuesta(estado string) *Respuesta {
	respuesta := &Respuesta{
		estado: estado,
	}
	return respuesta
}

func (r *Respuesta) esOk() bool {
	return r.estado == "OK"
}
