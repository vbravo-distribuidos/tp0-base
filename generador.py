import argparse
import copy

import yaml


class GeneradorDockerCompose:
    def __init__(self, clientes: int, ruta: str, ruta_plantilla: str):
        self.clientes = clientes
        self.ruta_salida = ruta
        self.plantilla = self.cargar_plantilla(ruta_plantilla)

    def cargar_plantilla(self, ruta: str):
        with open(ruta, "r") as file:
            plantilla = yaml.safe_load(file)
            return plantilla

    def generar_cliente(self, cliente: int):
        plantilla_cliente = self.plantilla["services"]["client1"]
        plantilla_nuevo_cliente = copy.deepcopy(plantilla_cliente)
        plantilla_nuevo_cliente["container_name"] = f"client{cliente}"
        plantilla_nuevo_cliente["environment"][0] = f"CLI_ID={cliente}"
        return plantilla_nuevo_cliente
    
    def generar_servidor(self, cantidad_clientes: int):
        plantilla_servidor = self.plantilla["services"]["server"]
        plantilla_nuevo_servidor = copy.deepcopy(plantilla_servidor)
        plantilla_nuevo_servidor["environment"][0] = f"CANTIDAD_CLIENTES={cantidad_clientes}"
        return plantilla_nuevo_servidor

    def generar(self):
        self.plantilla["services"]["server"] = self.generar_servidor(self.clientes)

        if self.clientes == 0:
            self.plantilla["services"].pop("client1")
            return 
        
        if self.clientes == 1:
            return 

        for i in range(1, self.clientes + 1):
            self.plantilla["services"][f"client{i}"] = self.generar_cliente(i)

    def guardar(self):
        with open(self.ruta_salida, "w+") as file:
            yaml.dump(self.plantilla, file)


def parsear_argumentos():
    parser = argparse.ArgumentParser(description="Generador de Docker Compose")
    parser.add_argument(
        "--clientes", type=int, required=True, help="Cantidad de clientes"
    )
    parser.add_argument(
        "--ruta_salida",
        type=str,
        required=True,
        help="Ruta del archivo docker compose de salida",
    )
    parser.add_argument(
        "--ruta_plantilla",
        type=str,
        required=True,
        help="Ruta de la plantilla del docker compose",
    )
    return parser.parse_args()


def main():
    args = parsear_argumentos()
    generador = GeneradorDockerCompose(
        args.clientes, args.ruta_salida, args.ruta_plantilla
    )
    generador.generar()
    generador.guardar()


if __name__ == "__main__":
    main()
