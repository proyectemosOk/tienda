from PIL import Image, ImageTk
import os
from tkinter import PhotoImage

def cargar_iconos(carpeta="img"):
    """
    Carga todas las imágenes de la carpeta especificada, redimensionándolas a 32x32 píxeles, en un diccionario.

    :param carpeta: Ruta de la carpeta donde se encuentran las imágenes (por defecto: "img").
    :return: Diccionario con el nombre del archivo (sin extensión) como clave y PhotoImage o ImageTk.PhotoImage como valor.
    """
    iconos = {}

    # Obtener la lista de archivos en la carpeta
    try:
        archivos = os.listdir(carpeta)
    except FileNotFoundError:
        print(f"Error: No se encontró la carpeta '{carpeta}'.")
        return iconos

    # Filtrar archivos con extensiones compatibles
    extensiones_validas = {".png", ".gif", ".ppm", ".pgm", ".jpg"}
    archivos_img = [archivo for archivo in archivos if os.path.splitext(archivo)[1].lower() in extensiones_validas]

    # Cargar cada archivo como PhotoImage o ImageTk.PhotoImage
    for archivo in archivos_img:
        nombre, _ = os.path.splitext(archivo)  # Obtener el nombre sin extensión
        ruta = os.path.join(carpeta, archivo)  # Crear la ruta completa

        try:
            # Abrir la imagen
            img = Image.open(ruta)
            # Redimensionar a 32x32 píxeles
            img = img.resize((64, 64), Image.LANCZOS)
            # Convertir la imagen redimensionada en ImageTk.PhotoImage
            iconos[nombre] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar '{ruta}': {e}")

    return iconos
