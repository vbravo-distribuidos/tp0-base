from common.respuesta import Respuesta
from common.utils import Bet

DELIMITADOR = ","


def apuesta_a_string(apuesta: Bet) -> str:
    campos = [
        str(apuesta.agency),
        apuesta.first_name,
        apuesta.last_name,
        apuesta.document,
        str(apuesta.birthdate),
        str(apuesta.number),
    ]
    return DELIMITADOR.join(campos)


def apuesta_desde_string(apuesta_str: str) -> Bet:
    campos = apuesta_str.split(DELIMITADOR)
    return Bet(campos[0], campos[1], campos[2], campos[3], campos[4], campos[5])


def respuesta_a_string(respuesta: Respuesta) -> str:
    return respuesta.estado


def respuesta_desde_string(respuesta_str: str) -> Respuesta:
    return Respuesta(estado=respuesta_str)
