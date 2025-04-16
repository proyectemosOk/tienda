import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class VistaProductos:
    def __init__(self, ver_frame_productos, producto, img_productos, ticket, colum=5):
        self.colum = colum
        self.ticket = ticket
        self.ver_frame_productos = ver_frame_productos
        self.img_productos = img_productos
        self.producto = producto

        # Colores y estilos
        self.colors = {
            "fondo": "#FFFFFF",
            "borde": "#E0E0E0",
            "texto": "#333333",
            "descripcion": "#666666",
            "stock": "#CC4444",
            "precio": "#1A73E8",
            "boton": "#4CAF50",
            "boton_hover": "#45A049",
            "borde_hover": "#1A73E8",
        }

        # Crear el frame del producto
        self.frame_producto = ctk.CTkFrame(
            self.ver_frame_productos,
            corner_radius=20,
            fg_color=self.colors["fondo"],
            border_width=1,
            border_color=self.colors["borde"]
        )
        self.frame_producto.grid_propagate(False)
        self.frame_producto.configure(width=130, height=200)

        # Obtener imagen del producto
        self.icono = self.img_productos.get(str(self.producto[-1]), self.img_productos["img"])

        # Contenedor para la imagen
        imagen_frame = ctk.CTkFrame(self.frame_producto, fg_color="transparent")
        imagen_frame.pack(pady=(2, 3), padx=5, fill="x")

        ttk.Label(imagen_frame, image=self.icono, background=self.colors["fondo"]).pack(expand=True)

        # Crear etiquetas de información
        self.crear_etiqueta(self.producto[1], 14, "bold", self.colors["texto"], (0, 1))
        self.crear_etiqueta(self.producto[4], 12, "", self.colors["descripcion"], (1, 0), 7)
        self.crear_etiqueta(f"Stock: {self.producto[3]}", 10, "", self.colors["stock"], (1, 0), 7)
        self.crear_etiqueta(self.formatear_pesos(self.producto[2]), 16, "bold", self.colors["precio"], (1, 0))

        # Botón de agregar
        self.boton_agregar = ctk.CTkButton(
            self.frame_producto,
            text="Agregar",
            command=self.click,
            fg_color=self.colors["boton"],
            hover_color=self.colors["boton_hover"],
            font=("Arial", 12, "bold")
        )
        self.boton_agregar.pack(pady=(1, 1), padx=5)

        # Aplicar eventos


    def crear_etiqueta(self, texto, tamaño, estilo=None, color="#000000", padding=(0, 0), padx=0):
        """Función auxiliar para crear etiquetas de texto."""
        etiqueta = ctk.CTkLabel(
            self.frame_producto,
            text=texto,
            font=("Arial", tamaño, estilo) if estilo else ("Arial", tamaño),  # Evita pasar un string vacío
            text_color=color,
            wraplength=160
        )
        etiqueta.pack(pady=padding, padx=padx)
        return etiqueta

    def click(self, event=None):
        """Agregar item al ticket si hay stock"""
        if int(self.producto[3]) > 0:
            self.ticket.agregar_item(self.producto[0], self.producto[1], self.producto[2], self.producto[3], self.icono)
            self.boton_agregar.configure(fg_color="#2E7D32")
            self.ver_frame_productos.after(200, lambda: self.boton_agregar.configure(fg_color=self.colors["boton"]))

    def enter(self, event):
        """Resalta el frame al pasar el cursor"""
        event.widget.config(cursor="hand2")
        self.frame_producto.configure(border_width=2, border_color=self.colors["borde_hover"])

    def leave(self, event):
        """Restablece el estilo original"""
        event.widget.config(cursor="")
        self.frame_producto.configure(border_width=1, border_color=self.colors["borde"])

    def formatear_pesos(self, precio):
        """Formatea el precio con separadores de miles"""
        return f"$ {precio:,.0f}".replace(",", ".")
