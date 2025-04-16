import customtkinter as ctk
import tkinter as tk

class Item:
    def __init__(self, parent_frame, id_producto, nombre, precio,stock, actulizar_total, eliminar_item, iconos=None):
        """
        Clase para representar y controlar un item dentro del ticket de venta.
        """
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.cantidad = 1
        self.actulizar_total =  actulizar_total
        self.eliminar_item = eliminar_item
        self.iconos = iconos
        self.total_precio = int(self.cantidad) * int(self.precio)

        self.frame = ctk.CTkFrame(parent_frame, corner_radius=15, fg_color="white", border_width=2, border_color="#1A73E8")
        self.frame.pack(fill = "x", anchor = "n", pady=5, padx=5, ipady=5, ipadx=5)
        fuente_items = ("Arial", 20)
        fuente_items_1 = ("Arial", 12)
        # Imagen
        ctk.CTkLabel(
            self.frame,
            text="",
            image=self.iconos, 
            fg_color="transparent"
        ).grid(row = 0, column = 0, padx=7, pady=(7,0), rowspan = 3, stick = "ew")

        # Nombre del producto
        self.nombre_label = ctk.CTkLabel(self.frame, text=self.nombre,font = fuente_items, wraplength=200,fg_color="transparent", justify = "left", anchor="w", width=200)
        self.nombre_label.grid(row = 0, column = 1, padx=7, pady=(7,0), stick = "ew")

        # Precio total del producto
        self.precio_label = ctk.CTkLabel(self.frame, text=self.formatear_pesos(self.precio * self.cantidad),font = fuente_items_1, text_color="#2df321", justify = "left", anchor="w", width=200)
        self.precio_label.grid(row = 1, column = 1, padx=5, stick = "ew")

        # Stock del producto
        self.stock_label = ctk.CTkLabel(self.frame, text=f"Stock: {self.stock}",font = fuente_items_1, text_color="#f37e21", justify = "left", anchor="w", width=200)
        self.stock_label.grid(row = 2, column = 1, padx=5, stick = "ew")

        # Botón para restar cantidad
        self.menos_button = ctk.CTkButton(
            self.frame, text="-", corner_radius=12, width=5,font = fuente_items_1,
            command=self.restar,
            hover_color="#45a049",

        )
        self.menos_button.grid(row = 2, column = 2, padx=(2,2))

        # Entrada de cantidad
        self.var_cant = tk.StringVar()
        self.var_cant.set("1")
        self.cant_label= ctk.CTkEntry(
            self.frame, textvariable = self.var_cant, font = fuente_items,justify ="center",
            corner_radius=20, width=90
        )
        self.cant_label.grid(row = 0, column = 2, columnspan = 3, rowspan = 2, padx=7, pady=(7,0), stick = "nesw")
        # En el constructor, añade este enlace:
        self.cant_label.bind("<KeyRelease>", self.manejar_cambio_entrada)

        # Botón para sumar cantidad
        self.mas_button = ctk.CTkButton(
            self.frame, text="+", corner_radius=12, width=5,font = fuente_items_1,
            command=self.sumar,
            hover_color="#45a049",
        )
        self.mas_button.grid(row = 2, column = 3, padx=(2,2))

        # Botón para eliminar el item
        self.eliminar_button = ctk.CTkButton(
            self.frame, text = "X", corner_radius=10, width=5,font = fuente_items_1,
            command=self.eliminar,fg_color="red"
        )
        self.eliminar_button.grid(row = 2, column = 4, padx=(2,2))

    def manejar_cambio_entrada(self, event=None):
        """
        Maneja cambios manuales en la entrada de cantidad.
        """
        try:
            nueva_cantidad = int(self.var_cant.get())
            if nueva_cantidad < 0:
                raise ValueError("Cantidad negativa no permitida.")
            self.cantidad = nueva_cantidad
            self.actualizar_cantidad()
            if self.cantidad<=0:
                self.frame.destroy()
                self.eliminar_item(self.id)
        except ValueError:
            # Si hay un error, restablece la cantidad a su valor previo
            self.var_cant.set(self.cantidad)
    
    def actualizar_cantidad(self):
        """
        Actualiza la cantidad del item y su precio total.
        """
        #self.cant_label.configure(text = str(self.cantidad))
        self.precio_label.configure(text=self.formatear_pesos(self.precio * self.cantidad))
        self.total_precio = self.precio * self.cantidad
        self.actulizar_total()

    def eliminar(self):
        """
        Elimina el frame del item.
        """
        self.cantidad=1
        self.restar()
    
    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def restar(self):
        self.cantidad-=1
        self.var_cant.set(self.cantidad)
        self.actualizar_cantidad()
        if self.cantidad<=0:
            self.frame.destroy()
            self.eliminar_item(self.id)    

    def sumar(self):

        if self.cantidad+1<=self.stock:
            self.cantidad+=1
            self.var_cant.set(self.cantidad)
            self.actualizar_cantidad()


# Ejemplo de integración
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x600")
    parent_frame = ctk.CTkFrame(root)
    parent_frame.pack(fill="both", expand=True, padx=10, pady=10)

    item1 = Item(parent_frame, 1, "Producto 1", 10000, 2,"","")
    item2 = Item(parent_frame, 2, "Producto 2", 20000, 2,"", "")

    root.mainloop()
