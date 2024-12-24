from core.acciones import activar_central
from core.central import Central
from core.sensor import Sensor
from core.sirena import Sirena
from core.boton import Boton
from config.settings import SENSORES, SIRENAS, BOTONES
import time



if __name__ == "__main__":


    central = Central()

    central.configurar_central()

    central.activar_central()

    try:
        while central.activa:
            central.verificar_eventos()
            time.sleep(1)  # Evita el uso excesivo de la CPU
    except KeyboardInterrupt:
        print("Sistema apagado.")
        central.desactivar_central()
