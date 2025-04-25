import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class SesionSegunda(ctk.CTkFrame):
    def __init__(self, master, empresa,ir_a_tienda,inicio_sesion,**kwargs):
        self.ir_a_tienda =ir_a_tienda
        self.inicio_sesion = inicio_sesion
        self.empresa = empresa.upper()
        super().__init__(master, **kwargs)
        self.configure(corner_radius=20, fg_color="white", border_width=2, border_color="lightgray")
        self.crear_widgets()

    def crear_widgets(self):
        # Cabecera con botón de volver
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=5)
        
        # Botón de volver con un icono simple
        self.btn_volver = ctk.CTkButton(
            header_frame, 
            text="← Volver", 
            command=self.inicio_sesion,
            fg_color="transparent", 
            hover_color="#f0f0f0",
            text_color="#2196F3",
            width=100,
            corner_radius=8,
            border_width=0
        )
        self.btn_volver.pack(side="left", anchor="w")
        titulo = ctk.CTkLabel(self, text=self.empresa, font=("Arial", 24, "bold"), text_color="#00B4D8")
        titulo.pack(pady=(10, 20))

        self.entries = {}

        campos = [
            ("Usuario", "usuario", "Ingrese Usuario"),
            ("Contraseña", "contrasena", "Ingrese Contraseña")
        ]

        for texto, key, placeholder in campos:
            frame = ctk.CTkFrame(self, fg_color="transparent", width=150 )
            frame.pack(fill="x", pady=5, padx=20)
            label = ctk.CTkLabel(frame, text=texto, width=150, font = ("Arial", 14, "bold"), anchor="w")
            label.pack()
            entry = ctk.CTkEntry(frame, width=150, show="●" if key=="contrasena" else "", placeholder_text=placeholder)
            entry.pack(padx=(10, 0), expand=True, fill="x")
            self.entries[key] = entry

        boton_registro = ctk.CTkButton(
            self, text="Ir a la tienda", command=self.iniciar_sesion,
            fg_color="#2196F3", hover_color="#1976D2", text_color="white",
            corner_radius=10, height=40, width=100
        )
        boton_registro.pack(pady=(20, 10))

    def iniciar_sesion(self):
        usuario = self.entries["usuario"].get().strip()
        contrasena = self.entries["contrasena"].get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        self.ir_a_tienda(usuario, contrasena)
        
        

# 🔁 Punto de entrada para probarlo
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    app = SesionSegunda(root,"Proyectemos")
    root.title("Inicio de sesión - Segunda sesión")
    root.geometry("600x500")
    app.pack(expand=True, padx=20, pady=20)
    root.mainloop()
