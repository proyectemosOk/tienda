import tkinter as tk
from tkinter import ttk
from conexion_base import ConexionBase
from tienda import InterfazPrincipal
import crear_bd
import customtkinter as ctk
from cargar_iconos import cargar_iconos
from conexion_base import ConexionBase
from PIL import Image, ImageTk


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
        self.master.resizable(False, False)
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
        # Base de datos
        crear_bd.crear_tablas()
        self.db = ConexionBase("tienda.db")

        # Crear widgets
        self.crear_interfaz()
        self.master.deiconify() 
    
    def crear_interfaz(self):
        """
        Crea los widgets para el login con un diseño más moderno y atractivo.
        """
        # Frame principal con sombra y bordes redondeados
        self.frame_login_1 = ctk.CTkFrame(
            self.master, 
            corner_radius=20, 
            fg_color="white",  # Color de fondo claro
            border_width=2,
            border_color="lightgray"  # Borde sutil
        )
        self.frame_login_1.pack(
            expand=True, 
            padx=20, 
            pady=20, 
            ipadx=30, 
            ipady=30
        )

        # Frame interno para centrar los elementos
        self.frame_login = ctk.CTkFrame(
            self.frame_login_1, 
            fg_color="transparent"
            
        )
        self.frame_login.pack(expand=True)

        # Título con estilo más moderno
        titulo = ctk.CTkLabel(
            self.frame_login, 
            text="INICIAR SESIÓN", 
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        titulo.pack(pady=(0, 20))

        # Contenedor para los campos de entrada
        input_container = ctk.CTkFrame(
            self.frame_login, 
            fg_color="transparent"
        )
        input_container.pack(fill="x", padx=20)

        # Campo de usuario
        usuario_frame = ctk.CTkFrame(
            input_container, 
            fg_color="transparent"
        )
        usuario_frame.pack(fill="x", pady=10)

        usuario_icon = ctk.CTkLabel(
            usuario_frame, 
            image=self.iconos["usuario"], 
            text=""
        )
        usuario_icon.pack(side="left", padx=(0, 10))

        self.usuario_var = tk.StringVar()
        self.entry_usuario = ctk.CTkEntry(
            usuario_frame,
            #textvariable=self.usuario_var,
            placeholder_text="Ingrese Usuario",
            width=250,
            height=40,
            corner_radius=10,
            border_color="lightgray",
            border_width=1
        )
        self.entry_usuario.pack(side="left", expand=True, fill="x")

        # Campo de contraseña
        contrasena_frame = ctk.CTkFrame(
            input_container, 
            fg_color="transparent"
        )
        contrasena_frame.pack(fill="x", pady=10)

        contrasena_icon = ctk.CTkLabel(
            contrasena_frame, 
            image=self.iconos["password"], 
            text=""
        )
        contrasena_icon.pack(side="left", padx=(0, 10))

        self.contrasena_var = tk.StringVar()
        self.entry_contrasena = ctk.CTkEntry(
            contrasena_frame,
            #textvariable=self.contrasena_var,
            placeholder_text="Ingrese Contraseña",
            width=250,
            height=40,
            corner_radius=10,
            border_color="lightgray",
            border_width=1,
            show="*"  # Ocultar contraseña
        )
        self.entry_contrasena.pack(side="left", expand=True, fill="x")

        # Botón de inicio de sesión con estilo moderno
        self.boton_login = ctk.CTkButton(
            self.frame_login,
            text="Continuar",
            command=self.iniciar_sesion,
            #image=self.iconos["iniciar-sesion"],
            compound="left",
            fg_color="#4CAF50",  # Color de botón moderno
            hover_color="#45a049",
            text_color="white",
            corner_radius=10,
            height=40,
            width=250
        )
        self.boton_login.pack(pady=(20, 0))

    def iniciar_sesion(self):
        """
        Lógica de autenticación de usuario.
        """
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        #if not usuario or not contrasena:
        #    messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
        #    return

        resultado = self.db.seleccionar("usuarios", "rol", "nombre = ? AND contrasena = ?", (usuario, contrasena))
        self.abrir_interfaz_principal("1")
        
        """
        if resultado:
            rol = resultado[0][0]
            self.abrir_interfaz_principal(rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        """
    
    def abrir_interfaz_principal(self, rol):
        """
        Abre la interfaz principal después del inicio de sesión exitoso.
        """
        self.lista_productos = self.db.seleccionar("productos", "codigo, nombre, precio_venta, stock, categoria")
        if rol == "1":
            self.frame_login_1.destroy()
            InterfazPrincipal(self.master,self.menu, self.master)
            
        else:
            pass
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz_Principal(root)
    root.mainloop()
