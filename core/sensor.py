from gpiozero import DigitalInputDevice

class Sensor:
    def __init__(self, nombre, pin):
        super().__init__()
        self.nombre = nombre
        self.pin = pin
        self.estado = False
        self.activo = False

        self.sensor = DigitalInputDevice(pin)

        # Verificar la configuración del sensor
        print(f"{self.nombre} configurado en el pin {self.pin}")
        self.sensor.when_activated = self.detectar_evento


    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def detectar_evento(self):
        """Evento que se ejecuta cuando el sensor detecta un cambio de estado"""
        if self.sensor.is_active:
            self.estado = True
            print(f"{self.nombre} detectó un evento (Activo).")
        else:
            self.estado = False
            print(f"{self.nombre} detectó un evento (Inactivo).")


