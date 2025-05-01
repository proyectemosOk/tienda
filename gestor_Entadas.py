import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from conexion_base import ConexionBase
import tkinter as tk
from CTkMessagebox import CTkMessagebox

class GestorEntradas(tk.Toplevel):
    def __init__(self, parent_frame, actualizar_productos, usuario, tabla):
        super().__init__(parent_frame)
        self.master = parent_frame
        self.title("Gestor de Entradas por Proveedor")
        self.actualizar_productos = actualizar_productos
        self.usuario = usuario
        self.db = ConexionBase(tabla)

        # Tema y colores
        self.color_primario = "#3B82F6"
        self.color_secundario = "#2563EB"
        self.color_exito = "#10B981"
        self.color_exito_hover = "#059669"
        self.color_texto = "#1E293B"
        self.color_fondo = "#F8FAFC"
        self.color_borde = "#E2E8F0"

        # Configuración principal de la ventana
        self.geometry("1100x750")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        ctk.set_appearance_mode("light")

        # === CONTENEDOR PRINCIPAL CON SCROLL ===
        self.canvas = tk.Canvas(self, bg=self.color_fondo, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=self.color_fondo)
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.scrollable_window, width=e.width))

        self._configurar_scroll_mouse()

        self.main_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.color_fondo, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        for i in range(6):
            self.main_frame.grid_rowconfigure(i, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.titulo_label = ctk.CTkLabel(
            self.main_frame, 
            text="REGISTRO DE ENTRADA DE PRODUCTOS", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.color_primario
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 20))

        self._crear_frame_busqueda()
        self._crear_frame_factura() 
        self._crear_frame_productos()
        self._crear_tabla_productos()
        self._cargar_categorias()
        self._cargar_unidades()

        self._configurar_estilo_tabla()

        self.proveedor_entry.bind("<Return>", lambda e: self.buscar_proveedor())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.adelante_ventana()
        self.deiconify()
        self.codigo_producto_entry.focus_force()

    def _configurar_scroll_mouse(self):
        def _on_mousewheel(event):
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.delta < 0:
                self.canvas.yview_scroll(1, "units")

        def _on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", _on_mousewheel_linux)


    def _configurar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurar el estilo del Treeview
        style.configure("Treeview", 
                         background="#FFFFFF",
                         foreground=self.color_texto,
                         rowheight=28,
                         fieldbackground="#FFFFFF",
                         borderwidth=0)
        
        # Configurar el estilo del encabezado
        style.configure("Treeview.Heading",
                         background=self.color_primario,
                         foreground="white",
                         relief="flat",
                         font=('Arial', 10, 'bold'))
        
        # Cambiar color cuando se selecciona
        style.map("Treeview",
                   background=[('selected', '#E0F2FE')],
                   foreground=[('selected', self.color_primario)])

    def adelante_ventana(self):
        self.attributes("-topmost", True)
    
    def _cargar_categorias(self):
        categorias = self.db.seleccionar("categorias", "categoria")
        self.lista_categoria = [cat[0] for cat in categorias]
    
    def _cargar_unidades(self):
        unidades = self.db.seleccionar("unidades", "unidad")
        self.lista_unidad = [unidad[0] for unidad in unidades]
    
    def _crear_frame_busqueda(self):
        # Frame para búsqueda de proveedor con mejor diseño
        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color=self.color_borde)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Título de sección
        titulo_seccion = ctk.CTkLabel(
            search_frame, 
            text="DATOS DEL PROVEEDOR", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_primario
        )
        titulo_seccion.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(10, 5))
        
        # Separador
        separator = ctk.CTkFrame(search_frame, height=2, fg_color=self.color_borde)
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
        
        # Búsqueda de proveedor con mejor diseño
        ctk.CTkLabel(search_frame, text="Proveedor:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.proveedor_entry = ctk.CTkEntry(
            search_frame, 
            width=200, 
            placeholder_text="Ingrese código o nombre...",
            border_color=self.color_borde,
            corner_radius=8
        )
        self.proveedor_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5 ) 
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.buscar_proveedor,
            fg_color=self.color_primario,
            hover_color=self.color_secundario,
            corner_radius=8,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=2, column=2, sticky="w", padx=15, pady=5)
        
        self.nombre_proveedor_label = ctk.CTkLabel(
            search_frame, 
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.color_primario
        )
        self.nombre_proveedor_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=15, pady=(5, 10))
    
    def mostrar_toplevel_proveedor(self, callback):
        self.top_interfaz_proovedor = ctk.CTkToplevel(self)
        self.top_interfaz_proovedor.title("Registrar Nuevo Proveedor")
        self.top_interfaz_proovedor.attributes("-topmost", True)
        self.top_interfaz_proovedor.grid_rowconfigure(0, weight=1)
        self.top_interfaz_proovedor.grid_columnconfigure(0, weight=1)
        self.top_interfaz_proovedor.geometry("700x450")

        frame = ctk.CTkFrame(self.top_interfaz_proovedor, corner_radius=15, fg_color=self.color_fondo)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Título del formulario
        titulo = ctk.CTkLabel(
            frame, 
            text="REGISTRO DE NUEVO PROVEEDOR", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.color_primario
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        left_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color=self.color_borde)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=10)
        left_frame.grid_columnconfigure(0, weight=1)
        
        right_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color=self.color_borde)
        right_frame.grid(row=1, column=1, sticky="nsew", pady=10)
        right_frame.grid_columnconfigure(0, weight=1)

        # Campos izquierda con mejor diseño
        ctk.CTkLabel(left_frame, text="Código:*", font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=(15,0), padx=15, sticky="w")
        codigo_entry = ctk.CTkEntry(left_frame, corner_radius=8, border_color=self.color_borde)
        codigo_entry.grid(row=1, column=0, pady=(0,10), padx=15, sticky="ew")

        ctk.CTkLabel(left_frame, text="Nombre:*", font=ctk.CTkFont(size=12)).grid(row=2, column=0, pady=(10,0), padx=15, sticky="w")
        nombre_entry = ctk.CTkEntry(left_frame, corner_radius=8, border_color=self.color_borde)
        nombre_entry.grid(row=3, column=0, pady=(0,10), padx=15, sticky="ew")

        ctk.CTkLabel(left_frame, text="RUT:", font=ctk.CTkFont(size=12)).grid(row=4, column=0, pady=(10,0), padx=15, sticky="w")
        rut_entry = ctk.CTkEntry(left_frame, corner_radius=8, border_color=self.color_borde)
        rut_entry.grid(row=5, column=0, pady=(0,15), padx=15, sticky="ew")

        # Campos derecha con mejor diseño
        ctk.CTkLabel(right_frame, text="Dirección:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, pady=(15,0), padx=15, sticky="w")
        direccion_entry = ctk.CTkEntry(right_frame, corner_radius=8, border_color=self.color_borde)
        direccion_entry.grid(row=1, column=0, pady=(0,10), padx=15, sticky="ew")

        ctk.CTkLabel(right_frame, text="Teléfono:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, pady=(10,0), padx=15, sticky="w")
        telefono_entry = ctk.CTkEntry(right_frame, corner_radius=8, border_color=self.color_borde)
        telefono_entry.grid(row=3, column=0, pady=(0,10), padx=15, sticky="ew")

        ctk.CTkLabel(right_frame, text="Email:", font=ctk.CTkFont(size=12)).grid(row=4, column=0, pady=(10,0), padx=15, sticky="w")
        email_entry = ctk.CTkEntry(right_frame, corner_radius=8, border_color=self.color_borde)
        email_entry.grid(row=5, column=0, pady=(0,15), padx=15, sticky="ew")

        # Botón Guardar con mejor diseño
        def guardar_proveedor():
            codigo = codigo_entry.get().strip()
            nombre = nombre_entry.get().strip()
            rut = rut_entry.get().strip()
            direccion = direccion_entry.get().strip()
            telefono = telefono_entry.get().strip()
            email = email_entry.get().strip()

            if not codigo or not nombre:
                if not codigo:
                    codigo_entry.configure(border_color="red")
                if not nombre:
                    nombre_entry.configure(border_color="red")
                self.top_interfaz_proovedor.attributes("-topmost", False)
                CTkMessagebox(title="Error", message="Los campos Código y Nombre son obligatorios.", icon="cancel", master=self.top_interfaz_proovedor)
                self.top_interfaz_proovedor.attributes("-topmost", True)
                return

            codigo_entry.configure(border_color=self.color_borde)
            nombre_entry.configure(border_color=self.color_borde)

            callback({
                "codigo": codigo,
                "nombre": nombre,
                "rut": rut if rut else None,
                "direccion": direccion if direccion else None,
                "telefono": telefono if telefono else None,
                "email": email if email else None,
            })
            self.top_interfaz_proovedor.destroy()

        ctk.CTkButton(
            frame,
            text="Guardar Proveedor",
            command=guardar_proveedor,
            fg_color=self.color_exito,
            hover_color=self.color_exito_hover,
            corner_radius=8,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, columnspan=2, pady=20, padx=50, sticky="ew")

        self.top_interfaz_proovedor.attributes("-topmost", True)
        codigo_entry.focus()
        self.top_interfaz_proovedor.grab_set()

    def registrar_nuevo_proveedor(self, proveedor_data):
        try:
            self.db.insertar("proveedores", proveedor_data)
            self.attributes("-topmost", False)
            messagebox.showinfo("Éxito", "Proveedor registrado exitosamente.")
        except Exception as e:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {str(e)}")
        
    def _crear_frame_factura(self):
        # Frame para datos de factura con mejor diseño
        factura_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color=self.color_borde)
        factura_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        factura_frame.grid_columnconfigure(1, weight=1)
        
        # Título de sección
        titulo_seccion = ctk.CTkLabel(
            factura_frame, 
            text="DATOS DE LA FACTURA", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_primario
        )
        titulo_seccion.grid(row=0, column=0, columnspan=6, sticky="w", padx=15, pady=(10, 5))
        
        # Separador
        separator = ctk.CTkFrame(factura_frame, height=2, fg_color=self.color_borde)
        separator.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10, pady=(0, 10))
        
        # Primera fila con mejor diseño
        ctk.CTkLabel(factura_frame, text="N° Factura:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.factura_entry = ctk.CTkEntry(
            factura_frame, 
            width=150, 
            corner_radius=8,
            border_color=self.color_borde
        )
        self.factura_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(factura_frame, text="Fecha Emisión:", font=ctk.CTkFont(size=12)).grid(row=2, column=2, sticky="w", padx=15, pady=5)
        self.fecha_emision_entry = ctk.CTkEntry(
            factura_frame, 
            width=120,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.fecha_emision_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)
        self.fecha_emision_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(factura_frame, text="Fecha Vencimiento:", font=ctk.CTkFont(size=12)).grid(row=2, column=4, sticky="w", padx=15, pady=5)
        self.fecha_vencimiento_entry = ctk.CTkEntry(
            factura_frame, 
            width=120,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.fecha_vencimiento_entry.grid(row=2, column=5, sticky="w", padx=5, pady=5)
        self.fecha_vencimiento_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        
        # Segunda fila con mejor diseño
        ctk.CTkLabel(factura_frame, text="Tipo de Pago:", font=ctk.CTkFont(size=12)).grid(row=3, column=0, sticky="w", padx=15, pady=(15, 5))
        self.tipo_pago_combo = ctk.CTkComboBox(
            factura_frame, 
            values=self._obtener_tipos_pago(), 
            width=150,
            corner_radius=8,
            border_color=self.color_borde,
            dropdown_hover_color=self.color_primario
        )
        self.tipo_pago_combo.grid(row=3, column=1, sticky="w", padx=5, pady=(15, 5))
        
        ctk.CTkLabel(factura_frame, text="Monto Pagado:", font=ctk.CTkFont(size=12)).grid(row=3, column=2, sticky="w", padx=15, pady=(15, 5))
        self.monto_pagado_entry = ctk.CTkEntry(
            factura_frame, 
            width=120,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.monto_pagado_entry.grid(row=3, column=3, sticky="w", padx=5, pady=(15, 5))
        
        # Estado de pago con mejor diseño
        estado_frame = ctk.CTkFrame(factura_frame, fg_color="transparent")
        estado_frame.grid(row=3, column=4, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        
        self.estado_pago_var = tk.StringVar(value="PENDIENTE")
        
        ctk.CTkLabel(estado_frame, text="Estado:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 10))
        
        ctk.CTkRadioButton(
            estado_frame, 
            text="Pendiente", 
            variable=self.estado_pago_var, 
            value="PENDIENTE",
            fg_color=self.color_primario,
            border_color=self.color_primario
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            estado_frame, 
            text="Parcial", 
            variable=self.estado_pago_var, 
            value="PARCIAL",
            fg_color=self.color_primario,
            border_color=self.color_primario
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            estado_frame, 
            text="Pagado", 
            variable=self.estado_pago_var, 
            value="PAGADO",
            fg_color=self.color_primario,
            border_color=self.color_primario
        ).pack(side="left", padx=5)
        
    def _crear_frame_productos(self):
        # Frame para entrada de productos con mejor diseño
        productos_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#FFFFFF", border_width=1, border_color=self.color_borde)
        productos_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        productos_frame.grid_columnconfigure(1, weight=1)
        
        # Título de sección
        titulo_seccion = ctk.CTkLabel(
            productos_frame, 
            text="PRODUCTOS", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.color_primario
        )
        titulo_seccion.grid(row=0, column=0, columnspan=7, sticky="w", padx=15, pady=(10, 5))
        
        # Separador
        separator = ctk.CTkFrame(productos_frame, height=2, fg_color=self.color_borde)
        separator.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10, pady=(0, 10))
        
        # Primera fila - Búsqueda de producto
        search_prod_frame = ctk.CTkFrame(productos_frame, fg_color="transparent")
        search_prod_frame.grid(row=2, column=0, columnspan=7, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(search_prod_frame, text="Buscar producto:", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.buscar_multi_entry = ctk.CTkEntry(
            search_prod_frame, 
            width=350, 
            placeholder_text="Ingrese código, nombre o descripción...",
            corner_radius=8,
            border_color=self.color_borde
        )
        self.buscar_multi_entry.pack(side="left", padx=5)
        self.buscar_multi_entry.bind('<Return>', self.buscar_producto_multicampo)
        
        ctk.CTkButton(
            search_prod_frame,
            text="Buscar",
            command=lambda: self.buscar_producto_multicampo(),
            fg_color=self.color_primario,
            hover_color=self.color_secundario,
            corner_radius=8,
            height=30,
            width=100,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=10)
        
        # Detalles del producto
        detalles_frame = ctk.CTkFrame(productos_frame, fg_color="transparent")
        detalles_frame.grid(row=3, column=0, columnspan=7, sticky="ew", padx=15, pady=(10, 5))
        detalles_frame.grid_columnconfigure(1, weight=1)
        
        # Primera fila de detalles
        ctk.CTkLabel(detalles_frame, text="Código Producto:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.codigo_producto_entry = ctk.CTkEntry(
            detalles_frame, 
            width=150,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.codigo_producto_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.codigo_producto_entry.bind('<Return>', self.buscar_producto)
        
        ctk.CTkLabel(detalles_frame, text="Nombre:", font=ctk.CTkFont(size=12)).grid(row=0, column=2, sticky="w", padx=15, pady=5)
        self.nombre_producto_label = ctk.CTkEntry(
            detalles_frame, 
            state="readonly",
            width=250,
            corner_radius=8
        )
        self.nombre_producto_label.grid(row=0, column=3, sticky="w", padx=5, pady=5, columnspan=3)
        
        # Segunda fila de detalles
        ctk.CTkLabel(detalles_frame, text="Cantidad:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=5)
        self.cantidad_entry = ctk.CTkEntry(
            detalles_frame, 
            width=100,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.cantidad_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(detalles_frame, text="Precio Compra:", font=ctk.CTkFont(size=12)).grid(row=1, column=2, sticky="w", padx=15, pady=5)
        self.precio_compra_entry = ctk.CTkEntry(
            detalles_frame, 
            width=100,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.precio_compra_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(detalles_frame, text="Precio Venta:", font=ctk.CTkFont(size=12)).grid(row=1, column=4, sticky="w", padx=15, pady=5)
        self.precio_venta_entry = ctk.CTkEntry(
            detalles_frame, 
            width=100,
            corner_radius=8,
            border_color=self.color_borde
        )
        self.precio_venta_entry.grid(row=1, column=5, sticky="w", padx=5, pady=5)
        
        ctk.CTkButton(
            productos_frame,
            text="Agregar Producto",
            command=self.agregar_producto_lista,
            fg_color=self.color_primario, 
            hover_color=self.color_secundario,
            corner_radius=8,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=4, column=0, columnspan=7, sticky="e", padx=15, pady=10)

    def buscar_producto_multicampo(self, event=None):
        busqueda = self.buscar_multi_entry.get().strip()
        producto = self.db.seleccionar(
            "productos", "*",
            "codigo = ? OR nombre LIKE ? OR descripcion LIKE ?",
            (busqueda, f"%{busqueda}%", f"%{busqueda}%")
        )
        if not producto:
            # Asegurarse de que la ventana principal esté enfocada
            self.master.grab_set() 
            respuesta = messagebox.askyesno("Producto no encontrado", "¿Deseas registrar un nuevo producto?")
            if respuesta:
                self.agregar_producto_lista_1()
        else:
            self.agregar_producto_lista_1()
    def _crear_tabla_productos(self):
        # Frame para la tabla usando grid
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Crear Treeview
        columns = ('Código', 'Nombre', 'Cantidad', 'Precio Compra', 'Precio Venta', 'Subtotal')
        self.tabla = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configurar columnas
        col_widths = [100, 200, 80, 100, 100, 100]
        for col, width in zip(columns, col_widths):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=width, anchor='center')
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient='vertical', command=self.tabla.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scroll_y.set)
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tabla.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(xscrollcommand=scroll_x.set)
        
        self.tabla.grid(row=0, column=0, sticky="nsew")
        
        # Botón para finalizar entrada
        ctk.CTkButton(
            self.main_frame,
            text="Finalizar Entrada",
            command=self.finalizar_entrada,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).grid(row=5, column=0, pady=5, sticky="ew")

    def _obtener_tipos_pago(self):
        tipos = self.db.seleccionar("tipos_pago", "nombre")
        return [tipo[0] for tipo in tipos]
        
    def buscar_proveedor(self):
        codigo = self.proveedor_entry.get()
        proveedor = self.db.seleccionar("proveedores", "*","codigo = ? OR nombre = ? OR telefono = ?",
        (codigo, codigo, codigo,)
    )

        if proveedor:
            self.nombre_proveedor_label.configure(text=f"Nombre: {proveedor[0][2]}")
            self.proveedor_id = proveedor[0][0]
        else:
            self.attributes("-topmost", False)
            self.mostrar_toplevel_proveedor(self.registrar_nuevo_proveedor)
    
    def buscar_producto(self, event=None):
        codigo = self.codigo_producto_entry.get()
        producto = self.db.seleccionar("productos", "*", "codigo = ?", (codigo,))
        if producto:
            self.producto_actual = producto[0]
            self.nombre_producto_label.delete(0, 'end')
            self.nombre_producto_label.insert(0, f"{producto[0][2]}")
            # Pre-llenar precios
            self.precio_compra_entry.delete(0, 'end')
            self.precio_compra_entry.insert(0, str(producto[0][4]))
            self.precio_venta_entry.delete(0, 'end')
            self.precio_venta_entry.insert(0, str(producto[0][5]))
        else:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", "Producto no encontrado")
            self.nombre_producto_label.delete(0, 'end')
            self.nombre_producto_label.focus()
    
    def mostrar_toplevel_categoria_unidad(self, callback):
        self._cargar_unidades()
        self._cargar_categorias()
        # Crear Toplevel
        self.attributes("-topmost", False)
        
        top = ctk.CTkToplevel(self)
        top.title("Datos del Producto")
        top.attributes("-topmost", True)
        
        ctk.CTkLabel(top, text="Seleccione la Categoría:").pack(pady=5)
        categoria_combobox = ctk.CTkComboBox(top, values=self.lista_categoria)
        categoria_combobox.pack(pady=5,padx =10)

        ctk.CTkLabel(top, text="Seleccione la Unidad:").pack(pady=5)
        unidad_combobox = ctk.CTkComboBox(top, values=self.lista_unidad)
        unidad_combobox.pack(pady=5)

        def guardar():
            categoria = categoria_combobox.get()
            unidad = unidad_combobox.get()
            try:
                self.db.insertar("categorias",{"categoria":categoria})
            except:
                pass
            try:
                self.db.insertar("unidades",{"unidad":unidad})
            except:
                pass
            if not categoria or not unidad:
                self.attributes("-topmost", False)
                messagebox.showerror("Error", "Debe seleccionar categoría y unidad.")
            else:
                callback(categoria, unidad)
                top.destroy()


        ctk.CTkButton(top, text="Guardar", command=guardar).pack(pady=10)
        top.deiconify()
            
    def agregar_producto_lista(self):
        try:
            codigo = self.codigo_producto_entry.get().strip()
            producto = self.db.seleccionar("productos", "*", "codigo = ?", (codigo,))
            print(producto)
            cantidad = float(self.cantidad_entry.get())
            precio_compra = float(self.precio_compra_entry.get())
            precio_venta = float(self.precio_venta_entry.get())
            subtotal = cantidad * precio_compra
            if producto == []:
                # Si el producto no existe, abrir la ventana Toplevel
                def registrar_producto(categoria, unidad):
                    self.db.insertar("productos", {
                        "codigo": codigo,
                        "nombre": self.nombre_producto_label.get(),
                        "descripcion": "",
                        "precio_compra":precio_compra,
                        "precio_venta":precio_venta,
                        "stock": 0,
                        "categoria": categoria,
                        "unidad": unidad
                    })
                    self.attributes()
                    self.attributes("-topmost", False)
                    messagebox.showinfo("Nuevo Producto", "El producto ha sido registrado exitosamente.")
                    self.producto_actual = self.db.seleccionar("productos", "*", "codigo = ?", (codigo,))[0]
                    self.agregar_producto_lista_1()
                    
                    
                self.mostrar_toplevel_categoria_unidad(registrar_producto)
                return
                
            # Agregar a la tabla
            self.tabla.insert('', 'end', values=(
                self.producto_actual[1],  # código
                self.producto_actual[2],  # nombre
                cantidad,
                precio_compra,
                precio_venta,
                subtotal
            ))
            self.limpiar_formulario()
            self.adelante_ventana()
            
        except ValueError:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", "Por favor complete todos los campos correctamente")
            self.adelante_ventana()
    
    def agregar_producto_lista_1(self):
        try:
            cantidad = float(self.cantidad_entry.get())
            precio_compra = float(self.precio_compra_entry.get())
            precio_venta = float(self.precio_venta_entry.get())
            subtotal = cantidad * precio_compra                
            # Agregar a la tabla
            self.tabla.insert('', 'end', values=(
                self.producto_actual[1],  # código
                self.producto_actual[2],  # nombre
                cantidad,
                precio_compra,
                precio_venta,
                subtotal
            ))
            
            # Limpiar campos
            self.limpiar_formulario()
            self.adelante_ventana()
            
        except ValueError:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", "Por favor complete todos los campos correctamente")
            self.adelante_ventana()
    def limpiar_formulario(self):
        # Limpiar campos
        self.codigo_producto_entry.delete(0, 'end')
        self.cantidad_entry.delete(0, 'end')
        self.nombre_producto_label.delete(0, 'end')
        self.precio_venta_entry.delete(0, 'end')
        self.precio_compra_entry.delete(0, 'end')
        self.codigo_producto_entry.focus()
    def finalizar_entrada(self):
        try:
            self.buscar_proveedor()
            # Validar que haya productos
            if len(self.tabla.get_children()) == 0:
                raise ValueError("No hay productos en la lista")
                
            # Calcular monto total
            monto_total = sum(float(self.tabla.item(item)['values'][5]) 
                            for item in self.tabla.get_children())
            
            # Insertar factura
            datos_factura = {
                "numero_factura": self.factura_entry.get(),
                "proveedor_id": self.proveedor_id,
                "fecha_emision": self.fecha_emision_entry.get(),
                "fecha_vencimiento": self.fecha_vencimiento_entry.get(),
                "tipo_pago": self.tipo_pago_combo.get(),
                "monto_total": monto_total,
                "monto_pagado": float(self.monto_pagado_entry.get() or 0),
                "estado_pago": self.estado_pago_var.get(),
                "usuario_id": self.usuario
            }
            
            self.db.insertar("facturas_proveedor", datos_factura)
            # Obtener el último ID de la tabla facturas_proveedor
            resultado = self.db.seleccionar("facturas_proveedor", "MAX(id)")
            ultimo_id = resultado[0][0] if resultado and resultado[0][0] is not None else 0

            # Generar el próximo ID
            factura_id = ultimo_id + 1
            # Insertar productos de la factura
            for item in self.tabla.get_children():
                valores = self.tabla.item(item)['values']
                producto_datos = {
                    "factura_id": factura_id,
                    "producto_id": valores[0],
                    "cantidad": valores[2],
                    "precio_compra": valores[3],
                    "precio_venta": valores[4]
                }
                self.db.insertar("detalle_factura", producto_datos)
                
                producto_datos = {
                    "id_producto": valores[0],
                    "cantidad": valores[2],
                    "precio_compra": valores[3],
                    "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.db.insertar("lotes_productos", producto_datos)
                # Actualizar stock del producto
                self.db.ejecutar_personalizado(
                    "UPDATE productos SET stock = stock + ? WHERE codigo = ?",
                    (valores[2], valores[0])
                )
            self.attributes("-topmost", False)
            messagebox.showinfo("Éxito", "Entrada registrada correctamente")
            self.actualizar_productos()
            self.destroy()

        except ValueError as e:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", str(e))
            self.adelante_ventana()

    def on_closing(self):
        self.attributes("-topmost", False)
        if messagebox.askokcancel("Salir", "¿Seguro que desea salir? Se perderán los cambios no guardados."):
            self.destroy()
        else:
            self.attributes("-topmost", True)
        


def actualizar():

    root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    gestor = GestorEntradas(root, actualizar, "1", "tienda_jfleong6_1.db")
    root.mainloop()