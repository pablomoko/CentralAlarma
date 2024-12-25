from config.settings import SENSORES, SIRENAS, BOTONES
from core.sensor import Sensor
from core.sirena import Sirena
from core.boton import Boton

import socket
import threading
import json


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


    def iniciar_socket_server(self, host='localhost', port=65432):
        """Inicia el servidor de sockets para comunicarse con Flask."""
        def socket_server():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen(5)
            print(f"Servidor de sockets escuchando en {host}:{port}")

            while True:
                conn, addr = server.accept()
                with conn:
                    print(f"Conexión recibida de {addr}")
                    data = conn.recv(1024).decode()
                    if data:
                        respuesta = self.procesar_comando(data)
                        conn.sendall(respuesta.encode())

        # Iniciar el servidor de sockets en un hilo separado
        self.socket_thread = threading.Thread(target=socket_server, daemon=True)
        self.socket_thread.start()

    def procesar_comando(self, comando):
        """Procesa los comandos recibidos por el socket."""
        try:
            if comando == "ESTADO":
                return json.dumps({"activa": self.activa, "eventos": [e.nombre for e in self.eventos]})
            elif comando == "ACTIVAR":
                self.activar_central()
                return json.dumps({"message": "Central activada"})
            elif comando == "DESACTIVAR":
                self.desactivar_central()
                return json.dumps({"message": "Central desactivada"})
            else:
                return json.dumps({"error": "Comando no reconocido"})
        except Exception as e:
            return json.dumps({"error": str(e)})