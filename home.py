import tkinter as tk
from tkinter import ttk
from cargar_iconos import *
from Cargar_imagenes import *
# from tienda import InterfazPrincipal
from RegistroFrame import RegistroFrame  
import math
import customtkinter as ctk
from animation_utils import *
from PIL import Image, ImageTk
import requests
from tkinter import messagebox
import json
import os
from segund_sesion import *
from conexion_base import *
import bcrypt 
from temp import *

class Interfaz_Principal:
    def __init__(self, master):
        """
        fondo = #008ADF
        """
        self.style = ttk.Style()
        
        self.style.configure('principal.TButton', font=('Helvetica', 12), anchor='w')
        self.style.configure('titulo.TLabel', font=('Helvetica', 30),foreground = "white", background="#008ADF")
        self.style.configure('producto.TLabel', font=('times', 20),foreground = "white", background="#008ADF", wraplength=150)
        self.style.configure('descripcion.TLabel', font=('times', 15),foreground = "white", background="#008ADF", wraplength=150)
        self.style.configure('precio.TLabel', font=('times', 25),foreground = "#1bdf00", background="#008ADF")
        self.style.configure('background.TFrame', background="#008ADF")
        self.master = master
        
        self.master.title("Tienda - Inicio de sesión")
        self.master.state("zoomed")
        self.master.config(bg = "white")
        #self.master.resizable(False, False)
        self.ancho_pantalla = self.master.winfo_screenwidth() 
        self.alto_pantalla = self.master.winfo_screenheight()

        # Cargar la imagen del ícono usando Pillow
        icon = Image.open("LOGO.ico")  # Cambia "LOGO.png" por tu archivo de ícono
        icon = icon.resize((32, 32))  # Redimensionar si es necesario

        # Convertir la imagen a un formato compatible con tkinter
        icon_tk = ImageTk.PhotoImage(icon)

        self.menu = tk.Menu(self.master)
        # Establecer el ícono de la ventana
        self.master.iconphoto(True, icon_tk)

        self.iconos = cargar_iconos()
        # Establecer el ícono de la ventana usando PIL para cargar la imagen

        self.img_productos = cargar_iconos("img_productos")
        ctk.set_appearance_mode("light")  # Opciones: "light", "dark", o "system"
        ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"

        # Frame principal
        self.frame_login_1 = ctk.CTkFrame(
            self.master,
            fg_color="#c6f1f8",
            border_width=0,
        )
        self.frame_login_1.pack(
            expand=True,
            fill="both"
        ) 

        # Crear widgets
        self._verificar_acceso_rapido()  
        self.master.deiconify()
        
    def _verificar_acceso_rapido(self):
        """
        Verifica si el archivo `info.json` existe en la ruta de la aplicación.
        Si existe, salta el inicio de sesión; si no, realiza el inicio de sesión normal.
        """
        ruta_info = os.path.join(os.environ.get("LOCALAPPDATA"), "Grupo JJ", "info.json")
        
        if os.path.exists(ruta_info):
            # Si el archivo existe, salta el inicio de sesión y carga la segunda sesión
            self._cargar_json()
            self.empresa = self._base_local.seleccionar("datos","descripcion","dato=?",("Empresa",))
            print(self.empresa)
            self.frame_segunda_sesion = SesionSegunda(self.frame_login_1, self.empresa[0][0], self.ir_a_tienda,self.crear_interfaz)
            self.cargar_imagen_derecha()
            self.mostrar_segunda_sesion()
        else:
            # Si no existe el archivo, realiza el inicio de sesión normal
            self.crear_interfaz()
    
    def _cargar_json(self):
        ruta_info = os.path.join(os.environ.get("LOCALAPPDATA"), "Grupo JJ", "info.json")
        with open(ruta_info, "r") as file:
            datos_usuario = json.load(file)
            self.usuario = datos_usuario.get("usuario")
            self.contrasena= datos_usuario.get("contrasena")
            base = datos_usuario.get("base")
            self._base_local = ConexionBase(base)
    
    def crear_interfaz(self):  
        # ---------- IZQUIERDA (Login) ----------
    
        self.frame_login = ctk.CTkFrame(self.frame_login_1, fg_color="white", corner_radius=20,border_width=2)
        

        # 🔷 Iconos arriba
        iconos_arriba = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        iconos_arriba.pack(pady=5)
        for icono in ["registradora", "carrito", "datafono"]:
            img = ctk.CTkLabel(iconos_arriba, image=self.iconos[icono], text="")
            img.pack(side="left", padx=5)

        # 🔷 Título app
        nombre_app = ctk.CTkLabel(self.frame_login, text="appTiendA",
                                font=("Arial", 32, "bold"), text_color="#00B4D8")
        nombre_app.pack(pady=(10, 30))

        # 🔷 Título del login
        titulo = ctk.CTkLabel(self.frame_login, text="INICIAR SESIÓN",
                            font=("Arial", 24, "bold"), text_color="#333333")
        titulo.pack(pady=(0, 20))

        # ---------- Campos de entrada ----------
        input_container = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        input_container.pack(fill="x", padx=20)

        # Usuario
        usuario_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        usuario_frame.pack(fill="x", pady=10)

        usuario_icon = ctk.CTkLabel(usuario_frame, image=self.iconos["usuario"], text="")
        usuario_icon.pack(side="left", padx=(0, 10))

        self.usuario_var = tk.StringVar()
        self.entry_usuario = ctk.CTkEntry(
            usuario_frame, placeholder_text="Ingrese Usuario",
            width=250, height=40, corner_radius=10,
            border_color="lightgray", border_width=1
        )
        self.entry_usuario.pack(side="left", expand=True, fill="x")

        # Contraseña
        contrasena_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        contrasena_frame.pack(fill="x", pady=10)

        contrasena_icon = ctk.CTkLabel(contrasena_frame, image=self.iconos["password"], text="")
        contrasena_icon.pack(side="left", padx=(0, 10))

        self.contrasena_var = tk.StringVar()
        self.entry_contrasena = ctk.CTkEntry(
            contrasena_frame, placeholder_text="Ingrese Contraseña",
            width=250, height=40, corner_radius=10,
            border_color="lightgray", border_width=1, show="●"
        )
        self.entry_contrasena.pack(side="left", expand=True, fill="x")

        # Botón
        self.boton_login = ctk.CTkButton(
            self.frame_login, text="Continuar", command=self.iniciar_sesion,
            fg_color="#4CAF50", hover_color="#45a049", text_color="white",
            corner_radius=10, height=40, width=250
        )
        self.boton_login.pack(pady=(0, 0))

        # 🔷 Texto inferior con "link"
        link_frame = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        link_frame.pack(pady=(0, 10))

        texto_info = ctk.CTkLabel(
            link_frame,
            text="Si aún no tiene su código de Empresa, solicítelo ",
            font=("Arial", 10, "bold"),
            text_color="black"
        )
        texto_info.pack(side="left")

        link_falso = ctk.CTkLabel(
            link_frame,
            text="Aquí",
            font=("Arial", 14, "underline"),
            text_color="#d82400",
            cursor = "hand2"
        )
        link_falso.pack(side="left")
        # Al entrar (hover)
        link_falso.bind("<Enter>", lambda e: link_falso.configure(text_color="#2e7d32"))

        # Al salir (leave)
        link_falso.bind("<Leave>", lambda e: link_falso.configure(text_color="#d82400"))
        link_falso.bind("<Button-1>", self.mostrar_registro)



        self.cargar_imagen_derecha()
        self.mostrar_frames()

    def mostrar_frames(self):
        # # Posiciones iniciales (fuera de la pantalla)
        self.frame_login.place(rely=0.5, anchor="e")
        # self.imagen_lateral_derecha.place(relx=0.28, rely=0.0, relheight=1)
        
        deslizar_horizontal(
            widget=self.frame_login,
            desde_x=-0.5,
            hasta_x=0.28,
            es_relativo=True,
            duracion=800,
            master=self.master
        )
        
        # Simultáneamente deslizar la imagen lateral
        deslizar_horizontal(
            widget=self.imagen_lateral_derecha,
            desde_x=1.28,
            hasta_x=0.28,
            es_relativo=True,
            duracion=800,
            master=self.master
        )
    
    def cargar_imagen_derecha(self):
        img_path = "img/lat-der.jpg"
        imagen = Image.open(img_path)
        x,y = self.redimensionar_imagen_ajustada(imagen)

        print(f"Tamaño imagen redimensionada: {imagen.size}")  # Debug

        # Guarda la imagen CTk en un atributo para evitar recolección de basura
        self.imagen_ctk = ctk.CTkImage(light_image=imagen,size=(x,y))

        self.imagen_lateral_derecha = ctk.CTkLabel(
            self.frame_login_1,
            image=self.imagen_ctk,
            text=""
        )
        
    def redimensionar_imagen_ajustada(self, imagen: Image.Image) -> Image.Image:
        # Obtiene dimensiones del frame contenedor

        
        ancho_disp = self.ancho_pantalla-400
        alto_disp = self.alto_pantalla-30

        # Relación de aspecto original
        relacion_aspecto = imagen.height / imagen.width
        print(imagen.height, imagen.width)

        # Opciones de escalado
        # 1. Escalar por ancho disponible
        nuevo_ancho = ancho_disp
        nuevo_alto_por_ancho = int(nuevo_ancho * relacion_aspecto)

        # 2. Escalar por alto disponible
        nuevo_alto = alto_disp
        nuevo_ancho_por_alto = int(nuevo_alto / relacion_aspecto)

        # Verifica cuál opción cabe mejor dentro del frame
        if nuevo_alto_por_ancho <= alto_disp:
            return nuevo_ancho, nuevo_alto_por_ancho
        else:
            return nuevo_ancho_por_alto, nuevo_alto

    def iniciar_sesion(self):
        """
        Lógica de autenticación de usuario.
        """
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        # Validar que los campos no estén vacíos
        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Crear el cuerpo de la solicitud para enviar al servidor
        data = {
            "usuario": usuario,
            "contrasena": contrasena
        }

        # Enviar la solicitud POST al servidor
        try:
            response = requests.post("http://192.168.1.19:5001/login", json=data)
            
            # Verificar la respuesta del servidor
            if response.status_code == 200:
                # La respuesta es exitosa, se ha autenticado el usuario
                respuesta = response.json()
                if respuesta.get("mensaje") == "Login exitoso":
                    base = respuesta.get("base")
                    # messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                    self._base_local = ConexionBase(base)
                    empresa = self._base_local.seleccionar("datos","descripcion","dato=?",("Empresa",))
                    self.frame_segunda_sesion = SesionSegunda(self.frame_login_1, empresa[0][0], self.ir_a_tienda, self.regresar_inicio_sesion)
                    guardar_datos_usuario(usuario,respuesta.get("pass"),respuesta.get("base"))
                    self.ir_a_segunda_sesion()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            else:
                messagebox.showerror("Error", f"Error en la conexión: {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con el servidor: {e}")
    
    def mostrar_registro(self, event=None):
        """Este método realiza una transición animada vertical del frame de login al de registro."""
        print("Iniciando transición a registro")
        
        # Crear una nueva instancia de RegistroFrame si no existe
        if not hasattr(self, 'frame_registro') or self.frame_registro is None:
            self.frame_registro = RegistroFrame(self.frame_login_1, self.volver_a_login)
        # Opción 1: Usar la función de transición predefinida
        animar_transicion(
            frame_saliente=self.frame_login,
            frame_entrante=self.frame_registro,
            saliente_inicio={'relx': 0.28, 'rely': 0.5, 'anchor': "e"},
            saliente_fin={'relx': 0.28, 'rely': -1.5, 'anchor': "e"},
            entrante_inicio={'relx': 0.33, 'rely': 1.5, 'anchor': "e"},
            entrante_fin={'relx': 0.33, 'rely': 0.5, 'anchor': "e"},
            duracion=800,
            easing=ease_in_out_quad,
            master=self.master
        )
    
    def mostrar_segunda_sesion(self, event =None):
        
        # Crear una nueva instancia de RegistroFrame si no existe
        if not hasattr(self, 'frame_registro') or self.frame_registro is None:
            self.frame_segunda_sesion = SesionSegunda(self.frame_login_1, self.empresa[0][0], self.ir_a_tienda,self.crear_interfaz)
            self.frame_segunda_sesion.place(rely=0.5, anchor="e")
        deslizar_horizontal(
            widget=self.frame_segunda_sesion,
            desde_x=-0.5,
            hasta_x=0.28,
            es_relativo=True,
            duracion=800,
            master=self.master
        )
        # Simultáneamente deslizar la imagen lateral
        deslizar_horizontal(
            widget=self.imagen_lateral_derecha,
            desde_x=1.28,
            hasta_x=0.28,
            es_relativo=True,
            duracion=800,
            master=self.master
        )

    def volver_a_login(self, event=None):
        """Método para volver al formulario de login con animación inversa."""
        print("Volviendo a login")
        
        animar_transicion(
            frame_saliente=self.frame_registro,
            frame_entrante=self.frame_login,
            saliente_inicio={'relx': 0.33, 'rely': 0.5, 'anchor': "e"},
            saliente_fin={'relx': 0.33, 'rely': -1.5, 'anchor': "e"},
            entrante_inicio={'relx': 0.28, 'rely': 1.5, 'anchor': "e"},
            entrante_fin={'relx': 0.28, 'rely': 0.5, 'anchor': "e"},
            duracion=800,
            easing=ease_in_out_quad,
            master=self.master
        )
    
    def abrir_interfaz_principal(self, rol):
        """
        Abre la interfaz principal después del inicio de sesión exitoso.
        """
        self.lista_productos = self.db.seleccionar("productos", "codigo, nombre, precio_venta, stock, categoria")
        if rol == "1":
            self.frame_login_1.destroy()
            # InterfazPrincipal(self.master,self.menu, self.master)
            
        else:
            pass
    
    def ir_a_tienda(self, usuario, contrasena):
        resultado = self._base_local.validar_credenciales("usuarios", usuario, contrasena)
        
        if resultado["valido"]:
            messagebox.showinfo("Vamos bien", "vamos bien")
        else:
            messagebox.showinfo("Vamos mal", "vamos mal")
    def regresar_inicio_sesion(self):
        """Método para volver al formulario de login con animación inversa."""
        print("Volviendo a login")
        
        animar_transicion(
            frame_saliente=self.frame_segunda_sesion,
            frame_entrante=self.frame_login,
            saliente_inicio={'relx': 0.2, 'rely': 0.5, 'anchor': "center"},
            saliente_fin={'relx': 0.2, 'rely': -1.5, 'anchor': "center"},
            entrante_inicio={'relx': 0.28, 'rely': 1.5, 'anchor': "e"},
            entrante_fin={'relx': 0.28, 'rely': 0.5, 'anchor': "e"},
            duracion=800,
            easing=ease_in_out_quad,
            master=self.master
        )

    def ir_a_segunda_sesion(self):
         animar_transicion(
            frame_saliente=self.frame_login,
            frame_entrante=self.frame_segunda_sesion,
            saliente_inicio={'relx': 0.28, 'rely': 0.5, 'anchor': "e"},
            saliente_fin={'relx': 0.28, 'rely': -1.5, 'anchor': "e"},
            entrante_inicio={'relx': 0.2, 'rely': 1.5, 'anchor': "center"},
            entrante_fin={'relx': 0.2, 'rely': 0.5, 'anchor': "center"},
            duracion=800,
            easing=ease_in_out_quad,
            master=self.master
        )

    def finalizar_transicion_registro(self):
        """Método opcional para ajustar layouts después de la animación."""
        # Aquí puedes añadir configuraciones adicionales si es necesario
        # Por ejemplo, ajustar el tamaño, añadir scrollbars, etc.
        pass
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz_Principal(root)
    root.mainloop()