from flask import Flask, jsonify, request
import socket
import json
import subprocess
import os
import time

app = Flask(__name__)

SOCKET_HOST = 'localhost'
SOCKET_PORT = 65432

def enviar_comando_socket(comando):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SOCKET_HOST, SOCKET_PORT))
            s.sendall(comando.encode())
            data = s.recv(1024).decode()
            return json.loads(data)
    except Exception as e:
        return {"error": str(e)}

def alarma_ejecutandose():
    """Comprueba si el socket está activo para determinar si la alarma está ejecutándose."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SOCKET_HOST, SOCKET_PORT))
        return True
    except ConnectionRefusedError:
        return False

def iniciar_alarma():
    """Inicia el script si no está ejecutándose."""
    if not alarma_ejecutandose():
        # Calcula la ruta absoluta a 'run.py' en base al directorio raíz del proyecto
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Ir al directorio raíz
        ruta_run = os.path.join(base_dir, "core", "run.py")

        # Verifica que la ruta exista antes de intentar ejecutarla
        if not os.path.isfile(ruta_run):
            return {"error": f"El archivo {ruta_run} no existe"}

        # Ejecuta 'run.py' usando la ruta absoluta
        proceso = subprocess.Popen(
            ["python", ruta_run],
            cwd=base_dir,  # Cambia el directorio de trabajo al directorio raíz del proyecto
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Espera unos segundos para verificar si la alarma inicia correctamente
        for _ in range(10):
            time.sleep(1)
            if alarma_ejecutandose():
                return {"message": "Alarma iniciada"}

        # Si no logra iniciar, termina el proceso
        proceso.terminate()
        return {"error": "No se pudo iniciar la alarma: el socket no está disponible"}

    return {"message": "La alarma ya está ejecutándose"}




@app.route('/api/eventos', methods=['GET'])
def obtener_eventos():
    if not alarma_ejecutandose():
        return jsonify({"error": "La alarma no esta ejecutandose"}), 500
    return jsonify(enviar_comando_socket("ESTADO"))

@app.route('/api/activar', methods=['POST'])
def activar_alarma():
    if not alarma_ejecutandose():
        iniciar_alarma()
    return jsonify(enviar_comando_socket("ACTIVAR"))

@app.route('/api/desactivar', methods=['POST'])
def desactivar_alarma():
    if not alarma_ejecutandose():
        return jsonify({"error": "La alarma no esta ejecutandose"}), 500
    return jsonify(enviar_comando_socket("DESACTIVAR"))

@app.route('/api/sensores', methods=['GET'])
def obtener_sensores():
    return jsonify(enviar_comando_socket("SENSORES")), 200

@app.route('/api/botones', methods=['GET'])
def obtener_botones():
    return jsonify(enviar_comando_socket("BOTONES")), 200

@app.route('/api/sirenas', methods=['GET'])
def obtener_sirenas():
    return jsonify(enviar_comando_socket("SIRENAS")), 200




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
