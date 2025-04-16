import sqlite3
import customtkinter as ctk
from conexion_base import ConexionBase

class DatosApp(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.db = ConexionBase("tienda.db")

        # Interfaz
        self.create_widgets()
        self.dato_combo.set("")
        self.adelante_ventana()
    def adelante_ventana(self):
        self.attributes("-topmost", True)
        #self.attributes("-topmost", False)
    def create_widgets(self):
        # Lista desplegable para seleccionar los datos
        self.dato_label = ctk.CTkLabel(self, text="Seleccionar Dato:")
        self.dato_label.grid(row=0, column=0, padx=10, pady=10)

        self.dato_combo = ctk.CTkComboBox(self, values=self.obtener_datos(), command=self.cargar_descripcion)
        self.dato_combo.grid(row=0, column=1, padx=10, pady=10)

        # Campo de texto para editar la descripción
        self.descripcion_label = ctk.CTkLabel(self, text="Descripción:")
        self.descripcion_label.grid(row=1, column=0, padx=10, pady=10)

        self.descripcion_text = ctk.CTkEntry(self)
        self.descripcion_text.grid(row=1, column=1, padx=10, pady=10)

        # Botón para actualizar los datos
        self.actualizar_button = ctk.CTkButton(self, text="Actualizar", command=self.actualizar_dato)
        self.actualizar_button.grid(row=2, column=0, columnspan=2, pady=10)

    def obtener_datos(self):
        # Obtener los datos desde la base de datos
        lista = self.db.seleccionar("datos","dato")
        print(lista)
        return [row[0] for row in lista]

    def cargar_descripcion(self, dato):
        # Cargar la descripción del dato seleccionado
        descripcion = self.db.seleccionar("datos","descripcion","dato = ?", (dato,))[0][0]
        self.descripcion_text.delete(0, ctk.END)
        self.descripcion_text.insert(0, descripcion)

    def actualizar_dato(self):
        dato = self.dato_combo.get()
        nueva_descripcion = self.descripcion_text.get()

        # Actualizar la descripción en la base de datos
        self.db.ejecutar_consulta('''UPDATE datos SET descripcion = ? WHERE dato = ?''', (nueva_descripcion, dato))
        # Mostrar mensaje de éxito
        ctk.CTkLabel(self, text="Datos actualizados correctamente!").grid(row=3, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    # Crear la ventana principal
    root = ctk.CTk()
    app = DatosApp(root)

    root.mainloop()
