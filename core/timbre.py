from gpiozero import DigitalInputDevice
import time

class Timbre:
    def __init__(self, nombre, pin):
        self.nombre = nombre
        self.pin_salida = pin
        self.timbre = DigitalInputDevice(pin)

    def tocar(self):
        """Activa el timbre por 1 segundo."""
        self.timbre.on()
        print(f"{self.nombre} activado.")
        time.sleep(1)  # Mantenerlo activado por 1 segundo
        self.timbre.off()
        print(f"{self.nombre} desactivado.")
