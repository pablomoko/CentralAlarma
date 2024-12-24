from config.settings import SENSORES, SIRENAS, BOTONES
from core.sensor import Sensor
from core.sirena import Sirena
from core.boton import Boton

class Central():
    def __init__(self):
        self.activa = False
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

    def configurar_central(self):
        # Configurar sensores
        for sensor_conf in SENSORES:
            sensor = Sensor(sensor_conf["nombre"], sensor_conf["pin"])
            self.agregar_sensor(sensor)

        # Configurar sirenas
        for sirena_conf in SIRENAS:
            sirena = Sirena(sirena_conf["nombre"], sirena_conf["pin"])
            self.agregar_sirena(sirena)

            # Configurar botones con acciones
        for boton_conf in BOTONES:
            if boton_conf["nombre"] == "Botón Activar":
                accion = lambda: self.activar_central()
            elif boton_conf["nombre"] == "Botón Apagar":
                accion = lambda: self.desactivar_central()
            else:
                accion = None
            boton = Boton(boton_conf["nombre"], boton_conf["pin"], accion)
            self.agregar_boton(boton)

        return self



    def activar_central(self):

        # Activar sensores
        for sensor in self.sensores:
            sensor.activar()

        # Activar botones
        for boton in self.botones:
            boton.activar()

        self.activa = True

    def desactivar_central(self):
        self.activa = False
        self.desactivar_sirenas()

    def desactivar_sirenas(self):
        for sirena in self.sirenas:
            sirena.desactivar()

