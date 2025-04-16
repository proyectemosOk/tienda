import customtkinter as ctk
from tkinter import messagebox
from conexion_base import ConexionBase

class NuevoCliente(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.conexion = ConexionBase("tienda.db")
        self.title("Nuevo Cliente")
        self.geometry("400x350")

        # Etiquetas y campos de entrada
        ctk.CTkLabel(self, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_nombre = ctk.CTkEntry(self, width=250)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Tipo de Documento:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.combo_tipo_document = ctk.CTkComboBox(self, values=["Cédula", "RUT"], width=250)
        self.combo_tipo_document.grid(row=1, column=1, padx=10, pady=10)
        self.combo_tipo_document.set("Cédula")  # Establecer un valor predeterminado



        ctk.CTkLabel(self, text="Número:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_numero = ctk.CTkEntry(self, width=250)
        self.entry_numero.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_telefono = ctk.CTkEntry(self, width=250)
        self.entry_telefono.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(self, width=250)
        self.entry_email.grid(row=4, column=1, padx=10, pady=10)

        # Botón para guardar
        ctk.CTkButton(self, text="Guardar", command=self.guardar_cliente).grid(row=5, column=0, columnspan=2, pady=20)
        self.adelante_ventana()
    def adelante_ventana(self):
        self.attributes("-topmost", True)
        #self.attributes("-topmost", False)
    def guardar_cliente(self):
        # Obtiene los datos ingresados
        nombre = self.entry_nombre.get().strip()
        tipo_document = self.combo_tipo_document.get().strip()
        numero = self.entry_numero.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        # Validar campos requeridos
        if not nombre or not tipo_document or not numero:
            messagebox.showerror("Error", "Los campos Nombre, Tipo de Documento y Número son obligatorios.")
            return

        # Inserta en la base de datos
        datos = {
            "nombre": nombre,
            "tipo_document": tipo_document,
            "numero": numero,
            "telefono": telefono,
            "email": email,
        }
        try:
            self.conexion.insertar("clientes", datos)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.destroy()  # Cierra la ventana
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente.\n{e}")

# Ventana principal
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestión de Clientes")
    ctk.set_appearance_mode("light")  # Opciones: "light", "dark", o "system"
    ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"
    NuevoCliente(root)


    root.mainloop()
