from core.sensor import Sensor
from core.sirena import Sirena

class Central(Sensor):
    def __init__(self):
        self.sensores = []
        self.sirenas = []
        self.botones = []
        self.eventos = []


    def agregar_sensor(self, sensor):
        self.sensores.append(sensor)

    def agregar_sirena(self, sirena):
        self.sirenas.append(sirena)

    def agregar_boton(self, boton):
        self.botones.append(boton)

    def verificar_eventos(self):
        for sensor in self.sensores:
            if sensor.estado:
                print(f"Evento detectado por {sensor.nombre}")
                self.eventos.append(sensor)
                for sirena in self.sirenas:
                    sirena.activar()

    def desactivar_alarmas(self):
        for sirena in self.sirenas:
            sirena.desactivar()

