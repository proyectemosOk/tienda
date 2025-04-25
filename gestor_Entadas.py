import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from conexion_base import ConexionBase
import tkinter as tk

class GestorEntradas(tk.Toplevel):
    def __init__(self, parent_frame, actualizar_productos, usuario, tabla):
        super().__init__(parent_frame)
        self.master = parent_frame
        self.title("Gestor de Entradas por Proveedor")
        self.actualizar_productos = actualizar_productos
        self.usuario = usuario
        self.db = ConexionBase(tabla)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear los diferentes componentes
        self._crear_frame_busqueda()
        self._crear_frame_factura()
        self._crear_frame_productos()
        self._crear_tabla_productos()
        self._cargar_categorias()
        self._cargar_unidades()
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.adelante_ventana()
        self.deiconify()
        self.codigo_producto_entry.focus_force()
    
    def adelante_ventana(self):
        self.attributes("-topmost", True)
        #self.attributes("-topmost", False)
    
    def _cargar_categorias(self):
        categorias = self.db.seleccionar("categorias", "categoria")
        self.lista_categoria = [cat[0] for cat in categorias]
    
    def _cargar_unidades(self):
        unidades = self.db.seleccionar("unidades", "unidad")
        self.lista_unidad = [unidad[0] for unidad in unidades]
    
    def _crear_frame_busqueda(self):
        # Frame para búsqueda de proveedor
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        # Búsqueda de proveedor
        ctk.CTkLabel(search_frame, text="Proveedor:").pack(side="left", padx=5)
        self.proveedor_entry = ctk.CTkEntry(search_frame, width=100)
        self.proveedor_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.buscar_proveedor
        ).pack(side="left", padx=5)
        
        self.nombre_proveedor_label = ctk.CTkLabel(search_frame, text="")
        self.nombre_proveedor_label.pack(side="left", padx=5)
    
    def mostrar_toplevel_proveedor(self, callback):
        # Crear ventana self.top_interfaz_proovedorlevel
        self.top_interfaz_proovedor = ctk.CTkToplevel(self)
        self.top_interfaz_proovedor.title("Registrar Nuevo Proveedor")
        self.top_interfaz_proovedor.attributes("-topmost", True)


        # Crear marco principal
        frame = ctk.CTkFrame(self.top_interfaz_proovedor)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear las dos columnas
        left_frame = ctk.CTkFrame(frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right_frame = ctk.CTkFrame(frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Campos en la primera columna (Izquierda)
        ctk.CTkLabel(left_frame, text="Código:").grid(row=0, column=0, pady=5, sticky="w")
        codigo_entry = ctk.CTkEntry(left_frame,width=200)
        codigo_entry.grid(row=1, column=0, pady=5, sticky="ew")

        ctk.CTkLabel(left_frame, text="Nombre:").grid(row=2, column=0, pady=5, sticky="w")
        nombre_entry = ctk.CTkEntry(left_frame,width=200)
        nombre_entry.grid(row=3, column=0, pady=5, sticky="ew")

        ctk.CTkLabel(left_frame, text="RUT:").grid(row=4, column=0, pady=5, sticky="w")
        rut_entry = ctk.CTkEntry(left_frame,width=200)
        rut_entry.grid(row=5, column=0, pady=5, sticky="ew")

        # Campos en la segunda columna (Derecha)
        ctk.CTkLabel(right_frame, text="Dirección:").grid(row=0, column=0, pady=5, sticky="w")
        direccion_entry = ctk.CTkEntry(right_frame,width=200)
        direccion_entry.grid(row=1, column=0, pady=5, sticky="ew")

        ctk.CTkLabel(right_frame, text="Teléfono:").grid(row=2, column=0, pady=5, sticky="w")
        telefono_entry = ctk.CTkEntry(right_frame,width=200)
        telefono_entry.grid(row=3, column=0, pady=5, sticky="ew")

        ctk.CTkLabel(right_frame, text="Email:").grid(row=4, column=0, pady=5, sticky="w")
        email_entry = ctk.CTkEntry(right_frame,width=200)
        email_entry.grid(row=5, column=0, pady=5, sticky="ew")

        # Botón para guardar (centrado abajo)
        ctk.CTkButton(
            frame, text="Guardar", command=lambda: guardar_proveedor()
        ).grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")

        # Función para guardar el proveedor
        def guardar_proveedor():
            codigo = codigo_entry.get().strip()
            nombre = nombre_entry.get().strip()
            rut = rut_entry.get().strip()
            direccion = direccion_entry.get().strip()
            telefono = telefono_entry.get().strip()
            email = email_entry.get().strip()

            # Validar campos obligatorios
            if not codigo or not nombre:
                self.attributes("-topmost", False)
                messagebox.showerror("Error", "Los campos Código y Nombre son obligatorios.")
                return

            # Llamar al callback para guardar el proveedor
            callback({
                "codigo": codigo,
                "nombre": nombre,
                "rut": rut if rut else None,
                "direccion": direccion if direccion else None,
                "telefono": telefono if telefono else None,
                "email": email if email else None,
            })
            self.top_interfaz_proovedor.destroy()
        self.top_interfaz_proovedor.deiconify()  # Asegura que esté visible
        self.top_interfaz_proovedor.lift()       # La lleva al frente
        self.top_interfaz_proovedor.focus_force()  # Da foco a la ventana
        self.top_interfaz_proovedor.attributes("-topmost", True)

    def registrar_nuevo_proveedor(self, proveedor_data):
        try:
            # Insertar proveedor en la base de datos
            self.db.insertar("proveedores", proveedor_data)
            self.attributes("-topmost", False)
            messagebox.showinfo("Éxito", "Proveedor registrado exitosamente.")
        except Exception as e:
            self.attributes("-topmost", False)
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {str(e)}")
        
    def _crear_frame_factura(self):
        # Frame para datos de factura
        factura_frame = ctk.CTkFrame(self.main_frame)
        factura_frame.pack(fill="x", padx=5, pady=5)
        
        # Primera fila
        row1 = ctk.CTkFrame(factura_frame)
        row1.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row1, text="N° Factura:").pack(side="left", padx=5)
        self.factura_entry = ctk.CTkEntry(row1, width=100)
        self.factura_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Fecha Emisión:").pack(side="left", padx=5)
        self.fecha_emision_entry = ctk.CTkEntry(row1, width=100)
        self.fecha_emision_entry.pack(side="left", padx=5)
        self.fecha_emision_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(row1, text="Fecha Vencimiento:").pack(side="left", padx=5)
        self.fecha_vencimiento_entry = ctk.CTkEntry(row1, width=100)
        self.fecha_vencimiento_entry.pack(side="left", padx=5)
        self.fecha_vencimiento_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        
        # Segunda fila
        row2 = ctk.CTkFrame(factura_frame)
        row2.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row2, text="Tipo de Pago:").pack(side="left", padx=5)
        self.tipo_pago_combo = ctk.CTkComboBox(row2, values=self._obtener_tipos_pago())
        self.tipo_pago_combo.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Monto Pagado:").pack(side="left", padx=5)
        self.monto_pagado_entry = ctk.CTkEntry(row2, width=100)
        self.monto_pagado_entry.pack(side="left", padx=5)
        
        self.estado_pago_var = tk.StringVar(value="PENDIENTE")
        ttk.Radiobutton(row2, text="Pendiente", variable=self.estado_pago_var, 
                       value="PENDIENTE").pack(side="left", padx=5)
        ttk.Radiobutton(row2, text="Parcial", variable=self.estado_pago_var, 
                       value="PARCIAL").pack(side="left", padx=5)
        ttk.Radiobutton(row2, text="Pagado", variable=self.estado_pago_var, 
                       value="PAGADO").pack(side="left", padx=5)
        
    def _crear_frame_productos(self):
        # Frame para entrada de productos
        productos_frame = ctk.CTkFrame(self.main_frame)
        productos_frame.pack(fill="x", padx=5, pady=5)
        
        # Primera fila - Búsqueda de producto
        row1 = ctk.CTkFrame(productos_frame)
        row1.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row1, text="Código Producto:").pack(side="left", padx=5)
        self.codigo_producto_entry = ctk.CTkEntry(row1, width=200)
        self.codigo_producto_entry.pack(side="left", padx=5)
        #self.codigo_producto_entry.bind('<Return>', self.buscar_producto)
        self.codigo_producto_entry.bind('<Return>', self.buscar_producto)
        
        ctk.CTkLabel(row1, text="Nombre").pack(side="left", padx=5)
        self.nombre_producto_label = ctk.CTkEntry(row1, width=300)
        self.nombre_producto_label.pack(side="left", padx=5)
        
        # Segunda fila - Detalles del producto
        row2 = ctk.CTkFrame(productos_frame)
        row2.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row2, text="Cantidad:").pack(side="left", padx=5)
        self.cantidad_entry = ctk.CTkEntry(row2, width=100)
        self.cantidad_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Precio Compra:").pack(side="left", padx=5)
        self.precio_compra_entry = ctk.CTkEntry(row2, width=100)
        self.precio_compra_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Precio Venta:").pack(side="left", padx=5)
        self.precio_venta_entry = ctk.CTkEntry(row2, width=100)
        self.precio_venta_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            row2,
            text="Agregar Producto",
            command=self.agregar_producto_lista
        ).pack(side="left", padx=5)
        
    def _crear_tabla_productos(self):
        # Frame para la tabla
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear Treeview
        columns = ('Código', 'Nombre', 'Cantidad', 'Precio Compra', 'Precio Venta', 'Subtotal')
        self.tabla = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame, orient='vertical', command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Empaquetar
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        self.tabla.pack(fill='both', expand=True)
        
        # Botón para finalizar entrada
        ctk.CTkButton(
            self.main_frame,
            text="Finalizar Entrada",
            command=self.finalizar_entrada,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(pady=5)
        
    def _obtener_tipos_pago(self):
        tipos = self.db.seleccionar("tipos_pago", "nombre")
        return [tipo[0] for tipo in tipos]
        
    def buscar_proveedor(self):
        codigo = self.proveedor_entry.get()
        proveedor = self.db.seleccionar("proveedores", "*", "codigo = ? OR nombre = ?", (codigo,codigo,))
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
        

def actulizar():
    root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("light")  # Opciones: "light", "dark", o "system"
    ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"
    gestor = GestorEntradas(root,actulizar,"1", "tienda_jfleong6_1.db")

    root.mainloop()