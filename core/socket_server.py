# core/socket_server.py
import socket
import threading
import json
from core.central import Central

class SocketServer:
    def __init__(self, central, host='localhost', port=65432):
        self.central = central  # Instancia de la clase Central
        self.host = host
        self.port = port

    def iniciar(self):
        """Inicia el servidor de sockets para comunicarse con el cliente."""
        server_thread = threading.Thread(target=self._iniciar_socket_server, daemon=True)
        server_thread.start()

    def _iniciar_socket_server(self):
        """Servidor de sockets en un hilo separado."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Servidor de sockets escuchando en {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Conexión recibida de {addr}")
                data = conn.recv(1024).decode()
                if data:
                    respuesta = self.procesar_comando(data)
                    conn.sendall(respuesta.encode())

    def procesar_comando(self, comando):
        """Procesa los comandos recibidos por el socket."""
        try:
            if comando == "ESTADO":
                return json.dumps({"activa": self.central.activa, "eventos": [e.nombre for e in self.central.eventos]})
            elif comando == "ACTIVAR":
                self.central.activar_central()
                return json.dumps({"message": "Central activada"})
            elif comando == "DESACTIVAR":
                self.central.desactivar_central()
                return json.dumps({"message": "Central desactivada"})
            else:
                return json.dumps({"error": "Comando no reconocido"})
        except Exception as e:
            return json.dumps({"error": str(e)})
