# run.py dentro de core
from core.central import Central
from config.settings import SENSORES, SIRENAS, BOTONES
import time


def iniciar_central():
    central = Central()
    central.configurar_central()
    central.iniciar_socket_server()
    central.activar_central()

    try:
        while central.activa:
            central.verificar_eventos()
            time.sleep(1)  # Evita el uso excesivo de la CPU
    except KeyboardInterrupt:
        print("Sistema apagado.")
        central.desactivar_central()


if __name__ == "__main__":
    iniciar_central()
