import customtkinter as ctk
import tkinter as tk

class Item:
    def __init__(self, parent_frame, id_producto, nombre, precio, stock, actualizar_total, eliminar_item, iconos=None):
        self.id = id_producto
        self.nombre = nombre
        self.precio_base = precio
        self.precio_actual = precio
        self.stock = stock
        self.cantidad = 1
        self.actualizar_total = actualizar_total
        self.eliminar_item = eliminar_item
        self.iconos = iconos
        self.total_precio = int(self.cantidad) * int(self.precio_actual)

        # Configuración del frame principal
        self.frame = ctk.CTkFrame(parent_frame, corner_radius=15, fg_color="white", border_width=2, border_color="#1A73E8")
        self.frame.pack(anchor="n", pady=5, padx=5, ipady=5, ipadx=5)
        
        # Fuentes
        fuente_titulo = ("Arial", 16, "bold")
        fuente_texto = ("Arial", 14)
        fuente_precio = ("Arial", 14, "bold")

        # Imagen del producto (si existe)
        if self.iconos:
            ctk.CTkLabel(
                self.frame, text="", image=self.iconos, fg_color="transparent"
            ).grid(row=0, column=0, padx=7, pady=7, rowspan=3, sticky="nsew")

        # Nombre del producto
        self.nombre_label = ctk.CTkLabel(
            self.frame, text=self.nombre, font=fuente_titulo, 
            wraplength=200, fg_color="transparent", anchor="w"
        )
        self.nombre_label.grid(row=0, column=1, padx=5, pady=(5,0), sticky="ew", columnspan=3)

        # Sección de PRECIO UNITARIO
        ctk.CTkLabel(
            self.frame, text="Precio:", font=fuente_texto, 
            fg_color="transparent", anchor="w"
        ).grid(row=1, column=1, padx=5, sticky="w")
        
        self.precio_var = tk.StringVar()
        self.precio_var.set(str(self.precio_actual))
        self.precio_entry = ctk.CTkEntry(
            self.frame, textvariable=self.precio_var, font=fuente_texto,
            justify="center", width=100, corner_radius=10
        )
        self.precio_entry.grid(row=1, column=2, padx=5, sticky="ew")
        self.precio_entry.bind("<KeyRelease>", self.actualizar_precio)

        # Sección de CANTIDAD


        self.var_cant = tk.StringVar()
        self.var_cant.set("1")
        self.cant_entry = ctk.CTkEntry(
            self.frame, textvariable=self.var_cant, font=fuente_texto,
            justify="center", width=15, corner_radius=10
        )
        self.cant_entry.grid(row=0, column=3, columnspan=3, rowspan=2, ipadx=5, pady=(5,3), sticky="nesw")
        self.cant_entry.bind("<KeyRelease>", self.manejar_cambio_entrada)

        # Botones de cantidad (-/+)
        self.menos_button = ctk.CTkButton(
            self.frame, text="➖", width=5, font=fuente_texto,
            command=self.restar, hover_color="#FF5555"
        )
        self.menos_button.grid(row=2, column=3, padx=(2,2), pady=(0,5))

        self.mas_button = ctk.CTkButton(
            self.frame, text="➕", width=5, font=fuente_texto,
            command=self.sumar, hover_color="#55FF55"
        )
        self.mas_button.grid(row=2, column=4, padx=(2,5), pady=(0,5))

        # Botón para eliminar
        self.eliminar_button = ctk.CTkButton(
            self.frame, text="❌", width=5, font=fuente_texto,
            command=self.eliminar, fg_color="#FF3333", hover_color="#FF0000"
        )
        self.eliminar_button.grid(row=2, column=5, padx=5, pady=(0,5))

        # Sección de TOTAL
        ctk.CTkLabel(
            self.frame, text="Total:", font=fuente_texto,
            fg_color="transparent", anchor="w"
        ).grid(row=2, column=1, padx=5, pady=(0,5), sticky="w")

        self.precio_total_label = ctk.CTkLabel(
            self.frame, text=self.formatear_pesos(self.total_precio), 
            font=fuente_precio, text_color="#2df321"
        )
        self.precio_total_label.grid(row=2, column=2, padx=5, pady=(0,5), sticky="ew")

    def actualizar_precio(self, event=None):
        """Actualiza el precio cuando se modifica manualmente"""
        try:
            nuevo_precio = float(self.precio_var.get())
            self.precio_actual = nuevo_precio
            self.actualizar_cantidad()
        except ValueError as e:
            print(e)
            self.precio_var.set(str(self.precio_actual))

    def manejar_cambio_entrada(self, event=None):
        """
        Maneja cambios manuales en la entrada de cantidad.
        Ahora permite valores negativos.
        """
        try:
            nueva_cantidad = int(self.var_cant.get())
            self.cantidad = nueva_cantidad
            self.actualizar_cantidad()
            if self.cantidad == 0:
                self.frame.destroy()
                self.eliminar_item(self.id)
        except ValueError:
            self.var_cant.set(str(self.cantidad))
    
    def actualizar_cantidad(self):
        """Actualiza la cantidad del item y su precio total."""
        self.total_precio = self.precio_actual * self.cantidad
        self.precio_total_label.configure(text=self.formatear_pesos(self.total_precio))
        self.actualizar_total()

    def eliminar(self):
        """Elimina el frame del item."""
        self.frame.destroy()
        self.eliminar_item(self.id)
    
    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def restar(self):
        self.cantidad -= 1
        self.var_cant.set(str(self.cantidad))
        self.actualizar_cantidad()
        if self.cantidad == 0:
            self.frame.destroy()
            self.eliminar_item(self.id)    

    def sumar(self):
        """Suma cantidad sin validar stock"""
        self.cantidad += 1
        self.var_cant.set(str(self.cantidad))
        self.actualizar_cantidad()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x600")
    parent_frame = ctk.CTkFrame(root)
    parent_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_total_callback():
        print("Total actualizado")

    def eliminar_item_callback(item_id):
        print(f"Item {item_id} eliminado")

    item1 = Item(parent_frame, 1, "Producto 1", 10000, 2, actualizar_total_callback, eliminar_item_callback)
    item2 = Item(parent_frame, 2, "Producto 2", 20000, 2, actualizar_total_callback, eliminar_item_callback)

    root.mainloop()