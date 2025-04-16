import customtkinter as ctk
from tkinter import messagebox
from conexion_base import ConexionBase

class GestorDeGastos(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.conexion = ConexionBase("tienda.db")
        self.title("Gestor de Gastos")
        self.geometry("400x300")

        # Etiquetas y campos de entrada
        ctk.CTkLabel(self, text="Monto:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_monto = ctk.CTkEntry(self, width=250)
        self.entry_monto.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Descripción:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_descripcion = ctk.CTkEntry(self, width=250)
        self.entry_descripcion.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Método de Pago:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.combo_metodo_pago = ctk.CTkComboBox(
            self, 
            values=["Efectivo", "Tarjeta", "Transferencia"], 
            width=250
        )
        self.combo_metodo_pago.grid(row=2, column=1, padx=10, pady=10)
        self.combo_metodo_pago.set("Efectivo")  # Valor predeterminado

        # Botón para guardar
        ctk.CTkButton(self, text="Guardar Gasto", command=self.guardar_gasto).grid(row=3, column=0, columnspan=2, pady=20)

    def guardar_gasto(self):
        # Obtiene los datos ingresados
        monto = self.entry_monto.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        metodo_pago = self.combo_metodo_pago.get().strip()

        # Validar campos
        if not monto or not descripcion or not metodo_pago:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            monto = float(monto)  # Validar que el monto sea numérico
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        # Inserta en la base de datos
        datos = {
            "monto": monto,
            "descripcion": descripcion,
            "metodo_pago": metodo_pago,
        }
        try:
            self.conexion.insertar("gastos", datos)
            messagebox.showinfo("Éxito", "Gasto registrado correctamente.")
            self.destroy()  # Cierra la ventana
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el gasto.\n{e}")

# Configuración principal
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestión de Gastos")

    def abrir_gestor_de_gastos():
        GestorDeGastos(root)

    # Botón para abrir el gestor de gastos
    btn_gestor_gastos = ctk.CTkButton(root, text="Nuevo Gasto", command=abrir_gestor_de_gastos)
    btn_gestor_gastos.pack(pady=20)

    root.mainloop()
