from conexion_base import ConexionBase
from crear_widgets import Tabla_filtro
import tkinter as tk

def main():
    # Crear una instancia de la base de datos
    db = ConexionBase("tienda_jfleong6_1.db")
    
    # Seleccionar los datos de la tabla productos
    datos = db.seleccionar("productos", "id, codigo, nombre, descripcion")
    
    # Inicializar la ventana principal de Tkinter
    ventana = tk.Tk()
    ventana.title("Tabla Dinámica de Productos")
    
    # Definir nombres y anchos de columnas para la tabla
    nombre_columnas = ["ID", "Código", "Nombre", "Descripción"]
    ancho_columnas = [50, 100, 200, 300]
    
    # Crear una instancia de la tabla filtro
    tabla = Tabla_filtro(
        parent=ventana,
        datos=datos,
        nombre_columnas=nombre_columnas,
        ancho_columnas=ancho_columnas,
        funcion=lambda: print("Elemento seleccionado"),  # Función de ejemplo para el botón
        buscar="producto",
        imagen=None  # Puedes proporcionar una imagen si lo deseas
    )
    
    # Ejecutar el loop principal de la ventana
    ventana.mainloop()

if __name__ == "__main__":
    main()
