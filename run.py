from core.central import Central
from core.sensor import Sensor
from core.sirena import Sirena
from config.settings import SENSORES, SIRENAS, BOTONES
import time

def configurar_central():
    central = Central()

    # Configurar sensores
    for sensor_conf in SENSORES:
        sensor = Sensor(sensor_conf["nombre"], sensor_conf["pin"])
        central.agregar_sensor(sensor)

    # Configurar sirenas
    for sirena_conf in SIRENAS:
        sirena = Sirena(sirena_conf["nombre"], sirena_conf["pin"])
        central.agregar_sirena(sirena)


    return central

if __name__ == "__main__":
    central = configurar_central()

    # Activar sensores
    for sensor in central.sensores:
        sensor.activar()

    try:
        while True:
            central.verificar_eventos()
            time.sleep(1)  # Evita el uso excesivo de la CPU
    except KeyboardInterrupt:
        print("Sistema apagado.")
        central.desactivar_alarmas()
