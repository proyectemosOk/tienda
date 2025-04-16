import tkinter as tk
from tkinter.ttk import *
from tkinter import *

class AgregarScrollVerticar:
    def __init__(self, ventana, bg_color="white"):
        # Configuración del canvas y scrollbars
        self.ventana = ventana
        self.bg_color = bg_color
        
        # Contenedor principal
        self.container = tk.Frame(ventana, bg=self.bg_color)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Canvas con scrollbar
        self.canvas = tk.Canvas(
            self.container, 
            bg=self.bg_color, 
            highlightthickness=0
        )
        self.vscrollbar = Scrollbar(
            self.container, 
            orient=tk.VERTICAL, 
            command=self.canvas.yview
        )
        
        # Configuración del scrollbar
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)

        # Posicionamiento de elementos
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame interno para contenido
        self.frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear ventana en el canvas
        self.canvas_frame = self.canvas.create_window(
            (0, 0), 
            window=self.frame, 
            anchor=tk.NW
        )

        # Bindings para actualizar región de scroll y comportamiento
        self.frame.bind('<Configure>', self.update_scroll_region)
        self.canvas.bind('<Configure>', self.resize_frame)
        
        # Habilitar scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def update_scroll_region(self, event=None):
        """Actualiza la región desplazable del canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def resize_frame(self, event):
        """Ajusta el ancho del frame interno al ancho del canvas"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def on_mousewheel(self, event):
        """Manejo suave del scroll con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def get_frame(self):
        """Devuelve el frame interno para agregar widgets"""
        return self.frame