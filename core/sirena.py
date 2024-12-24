from gpiozero import DigitalOutputDevice

class Sirena:
    def __init__(self, nombre, pin):
        self.nombre = nombre
        self.pin = pin
        self.activa = False
        self.sirena = DigitalOutputDevice(self.pin)
        print(f"Sirena {self.nombre} configurada en el pin {self.pin}")

    def activar(self):
        self.activa = True
        self.sirena.on()
        print(f"Sirena {self.nombre} activada!")

    def desactivar(self):
        self.activa = False
        self.sirena.off()
        print(f"Sirena {self.nombre} desactivada.")
