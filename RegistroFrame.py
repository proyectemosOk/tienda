import tkinter as tk
import customtkinter as ctk
import requests
import re
import uuid
from tkinter import messagebox
from temp import *
from conexion_base import *
import bcrypt 
from crear_bd import *
URL = "http://192.168.1.19:5001/registro"
class RegistroFrame(ctk.CTkFrame):
    def __init__(self, master, volver_inicio, **kwargs):
        self.volver_inicio = volver_inicio
        super().__init__(master, **kwargs)
        self.configure(corner_radius=20, fg_color="white", border_width=2, border_color="#e0e0e0")
        self.crear_widgets()
    
    def crear_widgets(self):
        # Cabecera con botón de volver
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=5)
        
        # Botón de volver con un icono simple
        self.btn_volver = ctk.CTkButton(
            header_frame, 
            text="← Volver", 
            command=self.volver_a_inicio,
            fg_color="transparent", 
            hover_color="#f0f0f0",
            text_color="#2196F3",
            width=100,
            corner_radius=8,
            border_width=0
        )
        self.btn_volver.pack(side="left", anchor="w")
        
        # Título centrado
        titulo = ctk.CTkLabel(
            self, 
            text="REGISTRO DE USUARIO", 
            font=("Arial", 24, "bold"), 
            text_color="#333333"
        )
        titulo.pack(pady=(5, 10))
        
        # Contenedor principal para los campos
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=30, pady=5, fill="both", expand=True)
        
        self.entries = {}
        
        campos = [
            ("Nombre completo", "nombre", False),
            ("Correo electrónico", "email", False),
            ("Teléfono", "telefono", False),
            ("Contraseña", "contrasena", True),
            ("Confirmar contraseña", "confirmar_contrasena", True)
        ]
        
        # Crear campos con mejor espaciado y diseño
        for i, (texto, key, es_contrasena) in enumerate(campos):
            frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            frame.pack(fill="x", pady=(0, 7))
            
            label = ctk.CTkLabel(
                frame, 
                text=texto, 
                font=("Arial", 12),
                text_color="#555555",
                anchor="w"
            )
            label.pack(side="top", anchor="w", pady=(0, 3))
            
            entry = ctk.CTkEntry(
                frame, 
                width=350, 
                height=35,
                corner_radius=8,
                border_width=1,
                border_color="#cccccc",
                fg_color="white",
                show="●" if es_contrasena else "",
                placeholder_text=f"Ingrese su {texto.lower()}"
            )
            entry.pack(side="top", fill="x")
            self.entries[key] = entry
        
        # Frame para la membresía
        membresia_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        membresia_frame.pack(fill="x", pady=(0, 10))
        
        membresia_label = ctk.CTkLabel(
            membresia_frame, 
            text="Membresía", 
            font=("Arial", 12),
            text_color="#555555",
            anchor="w"
        )
        membresia_label.pack(side="top", anchor="w", pady=(0, 3))
        
        self.membresia_combo = ctk.CTkComboBox(
            membresia_frame, 
            values=["Free", "Premium", "VIP"],
            width=350,
            height=35,
            corner_radius=8,
            border_width=1,
            border_color="#cccccc",
            button_color="#2196F3",
            dropdown_hover_color="#1976D2"
        )
        self.membresia_combo.set("Free")
        self.membresia_combo.pack(side="top", fill="x")
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=10, padx=30, fill="x")
        
        boton_registro = ctk.CTkButton(
            buttons_frame, 
            text="REGISTRAR",
            command=self.registrar_usuario,
            fg_color="#2196F3", 
            hover_color="#1976D2", 
            text_color="white",
            corner_radius=10, 
            height=45, 
            font=("Arial", 14, "bold")
        )
        boton_registro.pack(fill="x")
        
        # Separador
        separador = ctk.CTkFrame(buttons_frame, height=1, fg_color="#e0e0e0")
        separador.pack(fill="x", pady=7)
        
        # Frame para el texto y botón de inicio de sesión
        login_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        login_frame.pack(fill="x")
        
        texto_login = ctk.CTkLabel(
            login_frame, 
            text="¿Ya tienes una cuenta?", 
            text_color="#666666"
        )
        texto_login.pack(side="left", padx=(0, 10))
        
        boton_login = ctk.CTkButton(
            login_frame, 
            text="Iniciar sesión", 
            command=self.volver_a_inicio,
            fg_color="transparent", 
            # hover_color="transparent",
            text_color="#2196F3",
            font=("Arial", 12, "bold"),
            width=30
        )
        boton_login.pack(side="left")
    
    def validar_email(self, email: str) -> bool:
        """
        Valida si el formato del correo electrónico es correcto.
        """
        patron_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return bool(re.match(patron_email, email))
    
    def registrar_usuario(self):
        # Validación de campos
        datos = {k: entry.get().strip() for k, entry in self.entries.items()}
        datos["membresia"] = self.membresia_combo.get()
        datos["mac"]=uuid.getnode()
        
        # Validar que todos los campos estén llenos
        for campo, valor in datos.items():
            if valor == "":
                messagebox.showerror("Error", f"El campo {campo} es obligatorio.")
                self.entries[campo].focus()
                return
        if not self.validar_email(datos["email"]):
            messagebox.showerror("Error", f"Por favor, ingresa un correo electrónico válido.")
            self.entries["email"].focus()
            return
        # Validar que las contraseñas coincidan
        if datos["contrasena"] != datos["confirmar_contrasena"]:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            self.entries["confirmar_contrasena"].focus()
            return
        del datos["confirmar_contrasena"]
        print("Datos del nuevo usuario:", datos)
        
        # Aquí se implementaría la lógica para registrar al usuario en la base de datos
        try:
            response = requests.post(URL, json=datos)            
            # Manejar códigos de respuesta específicos
            if response.status_code == 409:
                messagebox.showerror("Error", "El correo ya está registrado")
                self.volver_a_inicio()
            elif response.status_code == 201:
                messagebox.showinfo("Éxito", f"Usuario registrado correctamente su usuario es: {response.json().get("mensaje")}")
                
                crear_tablas(response.json().get("base_datos"))
                cliente_temp = ConexionBase(response.json().get("base_datos"))
                dato_temp = { 
                    "usuario":  response.json().get("mensaje"),
                    "contrasena": response.json().get("pass"),
                    "rol":"admin"
                }
                guardar_datos_usuario(response.json().get("mensaje"), response.json().get("pass"),response.json().get("base_datos"))
                cliente_temp.insertar("usuarios",dato_temp)
                self.volver_a_inicio()
            else:
                messagebox.showerror("Error", f"Error en el servidor: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con el servidor: {e}")
    
    def volver_a_inicio(self):
        self.volver_inicio()

# Punto de entrada para probarlo
def inicio():
    print("vamos bien")
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Demo Registro de Usuario")
    root.geometry("500x700")
    
    frame = RegistroFrame(root, inicio)
    frame.pack(expand=True, fill="both", padx=20, pady=5)
    
    root.mainloop()