import os
import json

# Función para guardar los datos del usuario en un archivo JSON
def guardar_datos_usuario(usuario, contrasena, base):

    # Datos a almacenar
    datos_usuario = {
        "usuario": usuario,
        "contrasena": contrasena, 
        "base":base,
    }

    # Ruta del archivo JSON donde se guardarán los datos
    ruta_json = os.path.join(os.environ.get("LOCALAPPDATA"), "Grupo JJ", "info.json")

    # Guardar los datos en el archivo JSON
    os.makedirs(os.path.dirname(ruta_json), exist_ok=True)  # Asegurar que la carpeta existe
    with open(ruta_json, "w") as file:
        json.dump(datos_usuario, file, indent=4)
    
    print(f"Datos de {usuario} guardados correctamente en {ruta_json}.")

