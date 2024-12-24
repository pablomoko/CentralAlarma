from gpiozero import Button

class Boton:
    def __init__(self, nombre, pin, accion :None):
        super().__init__()
        self.nombre = nombre
        self.pin = pin
        self.activo = False
        self.accion = accion
        self.boton = Button(pin)

        if self.accion:
            self.boton.when_pressed = self.accion

        print(f"{self.nombre} configurado en el pin {self.pin}")

    def activar(self):
            self.activo = True

    def desactivar(self):
            self.activo = False