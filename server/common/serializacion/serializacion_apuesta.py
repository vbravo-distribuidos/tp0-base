from typing import List
from common.utils import Bet

DELIMITADOR_COLUMNA = ","
DELIMITADOR_FILA = "\n"


def apuestas_desde_string(apuestas_str: str) -> tuple[List[Bet], int]:
    apuestas = []
    cantidad_errores = 0

    if len(apuestas_str) == 0:
        return apuestas, cantidad_errores

    apuestas_str = apuestas_str.split(DELIMITADOR_FILA)
    for apuesta_str in apuestas_str:
        campos = apuesta_str.split(DELIMITADOR_COLUMNA)
        try:
            apuesta = Bet(campos[0], campos[1], campos[2], campos[3], campos[4], campos[5])
            apuestas.append(apuesta)
        except ValueError:
            cantidad_errores += 1
    return apuestas, cantidad_errores
