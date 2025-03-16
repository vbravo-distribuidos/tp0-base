#!/bin/bash
echo "Nombre del archivo de salida: $1"
echo "Cantidad de clientes: $2"
PLANTILLA_BASE="docker-compose-dev-base.yaml"
python generador.py --ruta_salida $1 --clientes $2 --ruta_plantilla $PLANTILLA_BASE