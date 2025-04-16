# Importaciones necesarias
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from agregarScroll import AgregarScrollVerticar
from generar_pdf_productos import generar_control_inventario
import webbrowser
from datetime import datetime

class GestorCierreInventario(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.title("Gestor de Cierre de Inventario")

        # Contenedor principal
        self.frame_encabezado = ctk.CTkFrame(self)
        self.frame_encabezado.pack(fill="x", padx=5, pady=5)
        self.geometry("800x700")

        # Contenedor principal con scroll
        frame = ctk.CTkFrame(self, bg_color="white")
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.frame_1 = AgregarScrollVerticar(frame)
        self.frame_1.canvas.config(bg="white")
        self.frame = self.frame_1.frame
        self.scroll_canvas = self.frame_1.canvas  # Referencia al canvas para desplazamiento

        # Contenedor botón
        self.frame_boton = ctk.CTkFrame(self)
        self.frame_boton.pack(fill="x", padx=5, pady=5)

        # Configura las columnas del encabezado y las celdas del contenido para que tengan el mismo peso (en este caso la misma proporción de ancho)
        self.frame_encabezado.grid_columnconfigure(0, weight=1, uniform="equal")
        self.frame_encabezado.grid_columnconfigure(1, weight=4, uniform="equal")
        self.frame_encabezado.grid_columnconfigure(2, weight=2, uniform="equal")
        self.frame_encabezado.grid_columnconfigure(3, weight=2, uniform="equal")
        self.frame_encabezado.grid_columnconfigure(4, weight=2, uniform="equal")
        self.frame_encabezado.grid_columnconfigure(5, weight=2, uniform="equal")

        self.frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.frame.grid_columnconfigure(1, weight=4, uniform="equal")
        self.frame.grid_columnconfigure(2, weight=2, uniform="equal")
        self.frame.grid_columnconfigure(3, weight=2, uniform="equal")
        self.frame.grid_columnconfigure(4, weight=2, uniform="equal")
        self.frame.grid_columnconfigure(5, weight=2, uniform="equal")
        # Etiqueta de encabezado
        ctk.CTkLabel(self.frame_encabezado, text="Cierre de Inventario", font=("Arial", 25)).grid(row=0, column=0, columnspan=6, pady=10)

        # Etiquetas para las columnas
        ctk.CTkLabel(self.frame_encabezado, text="ID", width=10).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_encabezado, text="Nombre", width=100, wraplength=150).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_encabezado, text="Precio", width=100).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_encabezado, text="Inicial", width=50).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_encabezado, text="Final", width=50).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_encabezado, text="Total", width=100).grid(row=1, column=5, padx=5, pady=5, sticky="w")

        # Cargar productos desde la base de datos
        self.entries = {}  # Diccionario para almacenar los Entry
        self.productos = self.db.ejecutar_personalizado("""SELECT p.id, COALESCE(p.nombre, '') || ' ' || COALESCE(p.descripcion, '') AS nombre_descripcion, p.precio_venta, p.stock + COALESCE(SUM(r.cantidad), 0) AS stock_total
        FROM productos p
        LEFT JOIN 
        detalles_ventas r ON p.id = r.producto_id AND r.estado = 1 GROUP BY  p.id, p.nombre, p.descripcion, p.precio_venta, p.stock""")
        venta_total =0
        # Crear filas dinámicamente
        for i, producto in enumerate(self.productos, start=2):
            self.entries[producto[0]]= ProductoRow(self.frame,i,producto,self.formatear_pesos,self.scroll_to_widget,self.actualizar_total_venta)
            # Mostrar ID y nombre,precio, inicial
            

        # Botón para guardar
        guardar_btn = ctk.CTkButton(self.frame_boton, text="Guardar", command=self.guardar_cierre_inventario)
        guardar_btn.grid(row=len(self.productos) + 2, column=0, padx =5, pady=5)
        # Botón para genrar pdf
        guardar_btn = ctk.CTkButton(self.frame_boton, text="Generar PDF", command=self.generar_pdf)
        guardar_btn.grid(row=len(self.productos) + 2, column=1, pady=5, padx= 50)

        ctk.CTkLabel(self.frame_boton,text = "Precio Venta:", font =("Arial", 35)).grid(row=len(self.productos) + 3, column=0, pady=5)
        self.total_venta = tk.StringVar()
        ctk.CTkLabel(self.frame_boton,textvariable=self.total_venta, font =("Arial", 35)).grid(row=len(self.productos) + 3, column=1, pady=5)

        self.total_entregado = tk.StringVar()
        self.Total_Entregado = self.db.ejecutar_personalizado("SELECT SUM(total) FROM entregas_diarias WHERE estado =1")[0][0]
        print(self.Total_Entregado)
        
        self.total_entregado.set(self.formatear_pesos(int(self.Total_Entregado)))

        ctk.CTkLabel(self.frame_boton,text = "Entregado:", font =("Arial", 35)).grid(row=len(self.productos) + 4, column=0, pady=5)
        ctk.CTkLabel(self.frame_boton,textvariable=self.total_entregado, font =("Arial", 35)).grid(row=len(self.productos) + 4, column=1, pady=5)
        ctk.CTkLabel(self.frame_boton,text = "Restante:", font =("Arial", 35)).grid(row=len(self.productos) + 5, column=0, pady=5)
        self.total_faltante = tk.StringVar()
        ctk.CTkLabel(self.frame_boton,textvariable=self.total_faltante, font =("Arial", 35)).grid(row=len(self.productos) + 5, column=1, pady=5)


    def scroll_to_widget(self, widget):

        # Obtener la posición y altura del widget
        widget_y = widget.winfo_y()
        widget_height = widget.winfo_height()

        # Obtener la altura del canvas y la posición de la vista
        canvas_height = self.scroll_canvas.winfo_height()
        canvas_yview = self.scroll_canvas.yview()

        # Verificar si el widget está completamente visible en el canvas
        if widget_y < 0:  # Si el widget está por encima de la vista actual
            # Mover el canvas hacia arriba
            self.scroll_canvas.yview_scroll(-10, "pixels")
            return  # Ya hemos desplazado, no necesitamos más desplazamiento

        elif widget_y + widget_height > canvas_height:  # Si el widget está por debajo de la vista actual
            # Mover el canvas hacia abajo
            self.scroll_canvas.yview_scroll(10, "pixels")
            return  # Ya hemos desplazado, no necesitamos más desplazamiento

    def on_key_release(self, event, id, entry):
        final = self.entries[id]["final"].get()
        print(final)
        venta = (int(self.entries[id]["inicial"])- int(final))*int(self.entries[id]["precio"])
        self.entries[id]["total"].set(self.formatear_pesos(venta))

    def generar_pdf(self):
        try:
            # Primero verifica si hay datos
            productos = self.db.seleccionar("productos", "id, COALESCE(nombre, '') || ' ' || COALESCE(descripcion, '') AS nombre_descripcion, precio_venta")
            
            if not productos:
                messagebox.showerror("Error", "No se encontraron productos en la base de datos")
                return
                
            # Imprime los datos para debug
            print("Productos obtenidos:", productos)
            
            # Genera el PDF
            generar_control_inventario("planilla.pdf", productos)
            webbrowser.open("planilla.pdf")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
            print("Error completo:", e)  # Para ver el error completo en la consola
    
    def actualizar_total_venta(self):
        self.Total_venta = 0
        
        for id in self.entries:
            self.Total_venta += self.entries[id].valor_venta
        self.total_venta.set(self.formatear_pesos(self.Total_venta))
        self.total_faltante.set(self.formatear_pesos(int(self.Total_venta) - int(self.Total_Entregado)))

    def guardar_cierre_inventario(self):
        """
        Guarda las cantidades finales ingresadas en la base de datos.
        """
        for id_producto in self.entries:
            cantidad = self.entries[id_producto].entry_final.get()
            if cantidad.isdigit():
                 consulta = f"UPDATE productos SET stock = ? WHERE id = ?"
                 self.db.ejecutar_personalizado(consulta,(cantidad, id_producto))
                 
            else:
                print(f"Cantidad inválida para el producto ID {id_producto}")
            self.db.insertar("cierre_inventario", {
"fecha":datetime.now().strftime("%Y-%m-%d"),
"total_venta":self.Total_venta.get(),
"total_entregado":self.Total_Entregado,
"faltante":self.Total_venta.get()-self.Total_Entregado
})
            consulta = f"UPDATE detalles_venta SET estado = 0"
            self.db.ejecutar_personalizado(consulta)
            consulta = f"UPDATE entregas_diarias SET estado = 0"
            self.db.ejecutar_personalizado(consulta)

        # Aquí puedes guardar el diccionario cierre_inventario en la base de datos
        

    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")
    

class ProductoRow:
    def __init__(self, frame, fila, producto, formatear_pesos,scroll_to_widget, actualizar_total_venta):
        self.frame = frame
        self.fila = fila
        self.producto = producto
        self.formatear_pesos = formatear_pesos        
        self.id_producto = producto[0]
        self.nombre_producto = producto[1]
        self.precio = producto[2]
        self.inicial = producto[3]
        self.scroll_to_widget = scroll_to_widget
        self.actualizar_total_venta = actualizar_total_venta
        self.valor_venta =0
        self.crear_fila()

    def crear_fila(self):
        """Crea las etiquetas y los campos de entrada en la fila."""
        # Mostrar ID y nombre, precio, inicial
        ctk.CTkLabel(self.frame, text=self.id_producto, width=10).grid(row=self.fila, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame, text=self.nombre_producto, width=100, wraplength=150).grid(row=self.fila, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame, text=self.formatear_pesos(self.precio), width=100, wraplength=150).grid(row=self.fila, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.frame, text=self.inicial, width=100).grid(row=self.fila, column=3, padx=5, pady=5, sticky="w")

        # Crear Entry para la cantidad final
        self.entry_final = ctk.CTkEntry(self.frame, width=50)
        self.entry_final.grid(row=self.fila, column=4, padx=5, pady=5)

        # Crear StringVar para el total
        self.x = tk.StringVar()
        self.x.set(self.formatear_pesos(0))
        

        # Mostrar el total en una etiqueta
        ttk.Label(self.frame, textvariable=self.x, state="disable", justify="right").grid(row=self.fila, column=5, padx=5, pady=5, sticky="w")

        # Asociar eventos con el Entry
        self.entry_final.bind("<FocusIn>", lambda event, widget=self.entry_final: self.scroll_to_widget_1(widget))
        self.entry_final.bind("<KeyRelease>", lambda event, widget=self.entry_final: self.on_key_release(event))

    def on_key_release(self, event):
        """Evento que se ejecuta cuando se libera una tecla en el campo 'final'."""
        try:
            self.valor_venta = (float(self.inicial) - float(self.entry_final.get()))*float(self.precio)
        except ValueError:
            self.valor_venta = 0
        self.x.set(self.formatear_pesos(self.valor_venta))
        self.actualizar_total_venta()

    def scroll_to_widget_1(self, widget):
        """Método que se ejecuta cuando el Entry recibe foco."""
        self.scroll_to_widget(widget)