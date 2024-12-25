from core.central import Central
from core.socket_server import SocketServer
import time


def iniciar_central():
    central = Central()
    central.configurar_central()

    central.activar_central()

    # Crear e iniciar el servidor de sockets
    socket_server = SocketServer(central)
    socket_server.iniciar()

    try:
        while central.activa:
            central.verificar_eventos()
            time.sleep(1)  # Evita el uso excesivo de la CPU
    except KeyboardInterrupt:
        print("Sistema apagado.")
        central.desactivar_central()


if __name__ == "__main__":
    iniciar_central()
