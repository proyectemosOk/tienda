# prueba_registro.py
import requests

# Cambia esta IP por la IP local del servidor donde corre tu server.py
URL = "http://192.168.1.19:5001/registro"

# Datos de prueba para registrar cliente
data = {
    "nombre": "Cliente Prueba",
    "email": "clienteprueba@example.com",
    "telefono": "555123456",
    "contrasena": "segura123",
    "membresia": "free"
}

try:
    response = requests.post(URL, json=data)
    print("Código de respuesta:", response.status_code)
    print("Respuesta del servidor:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Error al conectar con el servidor:", e)
