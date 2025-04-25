import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from conexion_base import ConexionBase
from datetime import datetime
from cargar_iconos import cargar_iconos
from PIL import Image, ImageTk
import os

from tkinter import simpledialog

import random
class GestorProductos(tk.Toplevel):
    def __init__(self, parent_frame, actulizar_productos, usuario, tabla):
        super().__init__(parent_frame)
        self.actulizar_productos = actulizar_productos
        self.usuario = usuario
        self.parent_frame = parent_frame
        self.db = ConexionBase(tabla)
         # Restaura la ventana al frente
        self.attributes("-topmost", True)
        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)        
        # Frames
        self.frame_1 = ctk.CTkFrame(self.frame)
        self.frame_1.pack(padx=10, pady=10, anchor = "n") 

        self.table_frame = ctk.CTkFrame(self.frame)
        self.table_frame.pack(fill = "y", expand = True, padx =5, pady = 5, anchor = "n")

        
        self.form_frame = ctk.CTkFrame(self.frame_1)
        self.form_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.stock_frame = ctk.CTkFrame(self.frame_1)
        #self.stock_frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "ew")
        
        self.image_frame = ctk.CTkFrame(self.frame_1)
        self.image_frame.grid(row = 0, column = 1, rowspan =2, padx = 10, pady = 10, sticky = "nesw")
        
        self._crear_formulario()
        self._crear_imagen_selector()
        #self._crear_control_stock()
        self._crear_tabla()
        self._cargar_datos()
        #self._cargar_categorias()
        #self._cargar_unidades()
        self.limpiar_formulario()
        
        self.imagen_path = None
        

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.adelante_ventana()
        
    def adelante_ventana(self):
        self.attributes("-topmost", True)
        #self.attributes("-topmost", False)
    
    def verificar_y_agregar_categoria_unidad(self, categoria, unidad):
        # Verificar y agregar categoría
        resultado_categoria = self.db.seleccionar("categorias","id",f"categoria = '{categoria}'")
        print(resultado_categoria)
        if resultado_categoria == []:
            self.db.insertar("categorias",{"categoria":categoria})
            print(f"Categoría '{categoria}' agregada.")

        # Verificar y agregar unidad      
        resultado_unidad = self.db.seleccionar("unidades","id",f"unidad = '{unidad}'")
        if resultado_unidad == []:
            # Solicitar símbolo al usuario
            simbolo = simpledialog.askstring("Nueva Unidad", f"Ingresa el símbolo para la unidad '{unidad}':")
            if simbolo:
                self.db.insertar("unidades",{"unidad":unidad,"simbolo":simbolo})
                print(f"Unidad '{unidad}' con símbolo '{simbolo}' agregada.")
            else:
                print(f"Unidad '{unidad}' no se agregó porque no se proporcionó un símbolo.")
        self._cargar()

    def on_closing(self):
        self.attributes("-topmost", False)
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            self.actulizar_productos()
            self.destroy()  # Cierra la ventana
        else:
            self.attributes("-topmost", True)
    
    def _crear_imagen_selector(self):       
        self.imagen_preview = ctk.CTkLabel(self.image_frame, text="Sin imagen", width=100, height=100)
        self.imagen_preview.pack(padx=5)
        
        self.seleccionar_imagen_btn = ctk.CTkButton(
            self.image_frame,
            text="Seleccionar imagen",
            command=self.seleccionar_imagen
        )
        self.seleccionar_imagen_btn.pack(side="bottom", fill= "x", padx=5)

    def _crear_formulario(self):
        # Fuente para las etiquetas
        font_label = ("Arial", 12)
        font_entry = ("Arial", 12)
        
        # Código
        ctk.CTkLabel(self.form_frame, text="Código:", font=font_label).grid(row=0, column=0, padx=5, pady=(2, 3))
        self.codigo_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=(2, 3))
        
        # Nombre
        ctk.CTkLabel(self.form_frame, text="Nombre:", font=font_label).grid(row=0, column=2, padx=5, pady=(2, 3))
        self.nombre_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.nombre_entry.grid(row=0, column=3, padx=5, pady=(2, 3))
        
        # Stock
        ctk.CTkLabel(self.form_frame, text="Stock:", font=font_label).grid(row=0, column=4, padx=5, pady=(2, 3))
        self.stock_entry = ctk.CTkEntry(self.form_frame, font=font_entry, state="disable")
        self.stock_entry.grid(row=0, column=5, padx=5, pady=(2, 3))
        
        
        
        # Precio de compra
        ctk.CTkLabel(self.form_frame, text="Precio de compra:", font=font_label).grid(row=1, column=0, padx=5, pady=(2, 3))
        self.precio_compra_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.precio_compra_entry.grid(row=1, column=1, padx=5, pady=(2, 3))
        
        # Precio de compra
        ctk.CTkLabel(self.form_frame, text="Precio de venta:", font=font_label).grid(row=1, column=2, padx=5, pady=(2, 3))
        self.precio_venta_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.precio_venta_entry.grid(row=1, column=3, padx=5, pady=(2, 3))
        
        # Categoría (ComboBox)
        ctk.CTkLabel(self.form_frame, text="Categoria:", font=font_label).grid(row=2, column=0, padx=5, pady=(2, 3))
        self.categoria_combobox = ctk.CTkComboBox(self.form_frame, values=[])
        self.categoria_combobox.grid(row=2, column=1, padx=5, pady=(2, 3))
        # Evento para desplegar al presionar flecha abajo
        self.categoria_combobox.bind("<Down>", lambda e: self.categoria_combobox.event_generate("<Button-1>"))

        
        # Unidad (ComboBox)
        ctk.CTkLabel(self.form_frame, text="Unidad:", font=font_label).grid(row=2, column=2, padx=5, pady=(2, 3))
        self.unidad_combobox = ctk.CTkComboBox(self.form_frame, values=[])
        self.unidad_combobox.grid(row=2, column=3, padx=5, pady=(2, 3))
        # Evento para desplegar la lista al presionar ↓
        self.unidad_combobox.bind("<Down>", self._desplegar_combobox)

        self._cargar()
        
        # Descripción
        ctk.CTkLabel(self.form_frame, text="Descripción:", font=font_label).grid(row=1, column=4, padx=5, pady=(2, 3),sticky = "w")
        self.descripcion_entry = ctk.CTkTextbox(self.form_frame, font=font_entry, height=50)
        self.descripcion_entry.grid(row=2, column=4, padx=5, pady=(2, 3), rowspan = 2, columnspan = 2,sticky = "news")
        
        # Botones
        self.btn_frame = ctk.CTkFrame(self.form_frame)
        self.btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Botón Agregar
        self.agregar_btn = ctk.CTkButton(
            self.btn_frame,
            text="Agregar",
            command=self.agregar_producto,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.agregar_btn.pack(side="left", padx=5)
        
        # Botón Modificar
        self.modificar_btn = ctk.CTkButton(
            self.btn_frame,
            text="Modificar",
            command=self.modificar_producto,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.modificar_btn.pack(side="left", padx=5)
        
        # Botón Eliminar
        self.eliminar_btn = ctk.CTkButton(
            self.btn_frame,
            text="Eliminar",
            command=self.eliminar_producto,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.eliminar_btn.pack(side="left", padx=5)
        
        # Botón Limpiar
        self.limpiar_btn = ctk.CTkButton(
            self.btn_frame,
            text="Limpiar",
            command=self.limpiar_formulario,
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        self.limpiar_btn.pack(side="left", padx=5)
    def _desplegar_combobox(self, event):
        print("hola")
        widget = event.widget
        widget.focus_set()
        widget.event_generate("<Button-1>")  # Simula clic para desplegar

    def _crear_tabla(self):
        # Crear Treeview
        columns = ('ID', 'Código', 'Nombre', 'Descripción', 'Precio de compra', 'Precio de venta', 'Stock', 'Categoría', 'Unidad')
        ancho = (25,50,250,250,110,100,50,90,70)
        self.tabla = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Configurar las columnas
        for col,anch in zip(columns, ancho):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anch)  # Ajusta el ancho según necesites
        
        # Agregar scrollbars
        scrollbar_y = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Empaquetar elementos
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        self.tabla.pack(fill='both', expand=True)
        
        # Vincular evento de selección
        self.tabla.bind('<<TreeviewSelect>>', self.seleccionar_producto)

    def _cargar_datos(self):
        # Limpiar tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        # Obtener productos de la base de datos
        productos = self.db.seleccionar("productos", "*")
        self.img_productos = cargar_iconos("img_productos") 
        
        # Insertar productos en la tabla
        for producto in productos:
            self.tabla.insert('', 'end', values=producto)
    
    def _cargar(self):
        self._cargar_categorias()
        self._cargar_unidades()
    
    def _cargar_categorias(self):
        categorias = self.db.seleccionar("categorias", "categoria")
        lista_categorias = [cat[0] for cat in categorias]
        self.categoria_combobox.configure(values=lista_categorias)

        if lista_categorias:
            self.categoria_combobox.set(lista_categorias[0])  # Opcional: valor por defecto
        
    def _cargar_unidades(self):
        unidades = self.db.seleccionar("unidades", "unidad")
        lista_unidades = [unidad[0] for unidad in unidades]
        self.unidad_combobox.configure(values=lista_unidades)

        if lista_unidades:
            self.unidad_combobox.set(lista_unidades[2])  # Valor por defecto opcional

    def seleccionar_producto(self, event):
        # Obtener el item seleccionado
        seleccion = self.tabla.selection()
        if not seleccion:
            return
            
        # Obtener valores del item seleccionado
        valores = self.tabla.item(seleccion[0])['values']        
        # Llenar el formulario con los valores
        self.limpiar_formulario()
        self.codigo_entry.insert(0, valores[1])
        self.nombre_entry.insert(0, valores[2])
        self.descripcion_entry.insert("1.0", valores[3])
        self.precio_compra_entry.insert(0, valores[4])
        self.precio_venta_entry.insert(0, valores[5])
        self.precio_compra_entry.configure(state = "disable")
        print(valores[0])
        self.stock_entry.insert(0, valores[6])
        self.categoria_combobox.set(valores[7])
        self.unidad_combobox.set(valores[8])
        if str(valores[0]) in self.img_productos:
            self.imagen_preview.configure(image=self.img_productos[str(valores[0])])
            self.imagen_preview.configure(text="")
        self.stock_entry.configure(state = "disable")

    def eliminar_producto(self):
        try:
            # Verificar si hay selección
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Por favor seleccione un producto para eliminar")
            
            # Obtener ID del producto seleccionado
            id_producto = self.tabla.item(seleccion[0])['values'][0]
            
            # Recuperar información del producto antes de eliminarlo
            producto = self.db.ejecutar_consulta("SELECT * FROM productos WHERE id = ?", (id_producto,))
            if not producto:
                raise ValueError("El producto seleccionado no existe.")
            producto = producto[0]  # Supone que devuelve una lista con un diccionario
            
            # Detalle del producto eliminado
            detalle = (
                f"Producto eliminado: ID={id_producto}, "
                f"Nombre='{producto['nombre']}', "
                f"Precio={producto['precio']}, "
                f"Stock={producto['stock']}, "
                f"Categoría='{producto['categoria']}'"
            )
            
            # Eliminar el producto de la base de datos
            self.db.eliminar("productos", "id = ?", (id_producto,))
            
            # Registrar la eliminación
            id_usuario = self.usuario  # Método para obtener el ID del usuario actual
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insertar("registro_modificaciones", {
                "id_producto": id_producto,
                "id_usuario": id_usuario,
                "fecha_hora": fecha_hora,
                "detalle": detalle
            })
            
            # Actualizar tabla
            self._cargar_datos()
            
            # Limpiar formulario
            self.limpiar_formulario()
            
        except ValueError as e:
            print(f"Error al eliminar producto: {str(e)}")
            self.adelante_ventana()
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            self.adelante_ventana()
 
    def _crear_control_stock(self):
        # Frame para control de stock
        # Entrada 
        ctk.CTkLabel(self.stock_frame, text="Entrada:", font=("Arial", 12)).pack(side="left", padx=5)
        self.cantidad_entry = ctk.CTkEntry(self.stock_frame, width=100)
        self.cantidad_entry.pack(side="left", padx=5)
        
        # Precio de compra
        ctk.CTkLabel(self.stock_frame, text="Precio de compra:", font=("Arial", 12)).pack(side="left", padx=5)
        self.entrada_precio_compra = ctk.CTkEntry(self.stock_frame, width=100)
        self.entrada_precio_compra.pack(side="left", padx=5)
        
        # Precio de venta
        ctk.CTkLabel(self.stock_frame, text="Precio de venta", font=("Arial", 12)).pack(side="left", padx=5)
        self.entrada_precio_venta = ctk.CTkEntry(self.stock_frame, width=100)
        self.entrada_precio_venta.pack(side="left", padx=5)
        
        # Observaciones
        ctk.CTkLabel(self.stock_frame, text="Observación:", font=("Arial", 12)).pack(side="left", padx=5)
        self.observacion_entry = ctk.CTkEntry(self.stock_frame, width=200)
        self.observacion_entry.pack(side="left", padx=5)
        
        self.aumentar_stock_btn = ctk.CTkButton(
            self.stock_frame,
            text="Aumentar Stock",
            command=self.aumentar_stock,
            fg_color="#9C27B0",
            hover_color="#7B1FA2"
        )
        self.aumentar_stock_btn.pack(side="left", padx=5)

    def seleccionar_imagen(self):
        self.attributes("-topmost", False)
        tipos_archivo = [('Imágenes', '*.png *.jpg *.jpeg *.gif *.bmp')]
        archivo = filedialog.askopenfilename(filetypes=tipos_archivo)
        
        if archivo:
            self.imagen_path = archivo
            # Mostrar previeww
            imagen = Image.open(archivo)
            imagen = imagen.resize((128, 128), resample=Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagen_preview.configure(image=imagen_tk, text = "")
            self.imagen_preview.image = imagen_tk
        self.attributes("-topmost", True)
    
    def aumentar_stock(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Seleccione un producto")
                
            id_producto = self.tabla.item(seleccion[0])['values'][0]
            cantidad = int(self.cantidad_entry.get())
            precio_compra = int(self.entrada_precio_compra.get())
            precio_venta = int(self.entrada_precio_venta.get())
            observacion = self.observacion_entry.get()
            
            if cantidad <= 0 and precio_compra <= 0 and precio_venta <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
                
            # Registrar entrada
            datos_entrada = {
                "producto_id": id_producto,
                "cantidad": cantidad,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "precio_compra":precio_compra,
                "precio_venta":precio_venta,
                "usuario": str(self.usuario),
                "observacion": observacion
            }
            self.db.insertar("registro_entradas", datos_entrada)
            
            # Actualizar stock
            stock_actual = self.db.seleccionar("productos", "stock", "id = ?", (id_producto,))[0][0]
            nuevo_stock = stock_actual + cantidad
            self.db.actualizar("productos", {"stock": nuevo_stock}, "id = ?", (id_producto,))
            
            # crear lote
            self.db.insertar("lotes_productos",{
                "id_producto":id_producto,
                "cantidad":cantidad,
                "precio_compra":precio_compra,
                "fecha_ingreso":datetime.now().strftime("%Y-%m-%d")
            })
            # Actualizar precio de venta tabla 
            self.db.actualizar("productos", {"precio_compra":precio_compra,"precio_venta":precio_venta}, "id = ?",(id_producto,))
            # Actualizar tabla y limpiar campos
            self._cargar_datos()
            self.limpiar_formulario()

            
        except ValueError as e:
            messagebox.showerror("Error stock"f"Error al aumentar stock: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error stock",f"Error inesperado: {str(e)}")

    def _guardar_imagen(self, codigo):
        if not self.imagen_path:
            return None
        id = self.db.seleccionar("productos","id","codigo = ?",((codigo),))[0][0]
        # Crear directorio si no existe
        if not os.path.exists("img_productos"):
            os.makedirs("img_productos")

        # Generar nombre de archivo
        extension = os.path.splitext(self.imagen_path)[1]
        nuevo_nombre = f"{id}{".png"}"
        ruta_destino = os.path.join("img_productos", nuevo_nombre)

        try:
            # Redimensionar la imagen a 128x128
            with Image.open(self.imagen_path) as img:
                img = img.resize((128, 128), Image.LANCZOS)  # Redimensionar con suavizado
                img.save(ruta_destino)  # Guardar la imagen redimensionada
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            
            self.adelante_ventana()
            return None

        return nuevo_nombre

    def agregar_producto(self):
        try:
            existente = self.db.seleccionar("productos", "codigo", "codigo = ?", self.codigo_entry.get())
            if len(existente) > 0:
                raise ValueError("Codigo ya Registrado")
            if self.codigo_entry.get().strip() == "":
                codigo_barras = self.generar_codigo_barras()
            else:
                codigo_barras =  self.codigo_entry.get().strip()
                
            # Obtener valores de los campos, dejando vacíos los opcionales
            datos = {
                "codigo": codigo_barras,
                "nombre": self.nombre_entry.get().strip(),
                "descripcion": self.descripcion_entry.get("1.0", "end-1c").strip() if self.descripcion_entry.get("1.0", "end-1c").strip() else "",
                "precio_compra": float(self.precio_compra_entry.get()) if self.precio_compra_entry.get().strip() else "",
                "precio_venta": float(self.precio_venta_entry.get()) if self.precio_venta_entry.get().strip() else "",
                "stock": int(self.stock_entry.get()) if self.stock_entry.get().strip() else "",
                "categoria": self.categoria_combobox.get().strip(),
                "unidad": self.unidad_combobox.get().strip()
            }

            # Verificar campos obligatorios
            if not all([datos["nombre"], datos["categoria"], datos["precio_compra"], datos["precio_venta"], datos["unidad"]]):
                messagebox.showerror("Error", "Complete los campos obligatorios")
                raise ValueError("Complete los campos obligatorios")

            self.verificar_y_agregar_categoria_unidad(self.categoria_combobox.get(), self.unidad_combobox.get())

            
            # Insertar producto en la base de datos
            try:
                self.db.insertar("productos", datos)

                # Registrar la acción de agregar producto
                id_usuario = self.usuario  # Método para obtener el ID del usuario actual
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detalle = (
                    f"Producto agregado: ID={self.codigo_entry.get()}, "
                    f"Nombre='{datos['nombre']}', "
                    f"Precio Compra='{datos['precio_compra']}', "
                    f"Precio Venta='{datos['precio_venta']}', "
                    f"Stock='{datos['stock']}', "
                    f"Categoría='{datos['categoria']}', "
                    f"Unidad='{datos['unidad']}'"
                )

                self.db.insertar("registro_modificaciones", {
                    "id_producto": self.codigo_entry.get(),
                    "id_usuario": id_usuario,
                    "fecha_hora": fecha_hora,
                    "detalle": detalle
                })

                if datos["stock"] and datos["precio_compra"]:
                    self.db.insertar("lotes_productos", {
                        "id_producto": self.codigo_entry.get(),
                        "cantidad": int(datos["stock"]),
                        "precio_compra": float(datos["precio_compra"]),
                        "fecha_ingreso": fecha_hora
                    })

                # Guardar imagen si existe
                nombre_imagen = self._guardar_imagen(datos["codigo"])
                if nombre_imagen:
                    datos["imagen"] = nombre_imagen

                # Actualizar datos en la interfaz y limpiar formulario
                self._cargar_datos()
                self.limpiar_formulario()
            except ValueError as e:
                print(e)
        except ValueError as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
            self.adelante_ventana()

    def modificar_producto(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Seleccione un producto para modificar")
                
            id_producto = self.tabla.item(seleccion[0])['values'][0]
            
            # Recuperar los datos actuales del producto antes de la actualización
            datos_anteriores = self.db.ejecutar_personalizado("SELECT * FROM productos WHERE id = ?", (id_producto,))
            if not datos_anteriores:
                raise ValueError("El producto seleccionado no existe.")
            datos_anteriores = datos_anteriores[0][1:]  # Supone que el resultado es una lista con un diccionario
            print(datos_anteriores)
            # Preparar los nuevos datos
            datos = {
                "codigo": self.codigo_entry.get(),
                "nombre": self.nombre_entry.get(),
                "descripcion": self.descripcion_entry.get("1.0", "end-1c").strip(),
                "precio_compra": float(self.precio_compra_entry.get()),
                "precio_venta": float(self.precio_venta_entry.get()),
                "stock": int(self.stock_entry.get()),
                "categoria": self.categoria_combobox.get(),
                "unidad": self.unidad_combobox.get()
            }
            datos_anteriores_1 = {}
            for columa, dato_viejo in zip(datos, datos_anteriores):
                datos_anteriores_1[columa] = dato_viejo

            # Actualizar imagen si se seleccionó una nueva
            self._guardar_imagen(datos["codigo"])


            # Detectar cambios y preparar el detalle
            cambios = []
            for columna, nuevo_valor in datos.items():
                valor_anterior = datos_anteriores_1.get(columna)
                if str(valor_anterior) != str(nuevo_valor):  # Comparar valores como cadenas
                    cambios.append(
                        f"Columna '{columna}': Antes='{valor_anterior}', Ahora='{nuevo_valor}'"
                    )

            # Si no hay cambios, detener el proceso
            if cambios:
                # Registrar la modificación
                id_usuario = self.usuario  # Método para obtener el ID del usuario actual
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detalle = "\n".join(cambios)  # Combinar los detalles de los cambios
                self.db.insertar("registro_modificaciones", {
                    "id_producto": id_producto,
                    "id_usuario": id_usuario,
                    "fecha_hora": fecha_hora,
                    "detalle": detalle
                })
            
            # Actualizar la base de datos
            self.db.actualizar("productos", datos, "id = ?", (id_producto,))

            
            # Actualizar datos en la interfaz y limpiar formulario
            self._cargar_datos()
            self.limpiar_formulario()
            
        except ValueError as e:
            print(f"Error al modificar producto: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    def limpiar_formulario(self):
        self._cargar_categorias()
        self._cargar_unidades()
        self.imagen_path = None
        self.stock_entry.configure(state = "normal")
        self.precio_compra_entry.configure(state = "normal")
        
        self.imagen_preview.configure(image=self.img_productos["img"])
        self.imagen_preview.configure(text="Sin imagen")
        #self.cantidad_entry.delete(0, 'end')
        #self.entrada_precio_compra.delete(0, 'end')
        #self.entrada_precio_compra.delete(0, 'end')
        #self.observacion_entry.delete(0, 'end')
        self.codigo_entry.delete(0, 'end')
        self.nombre_entry.delete(0, 'end')
        self.descripcion_entry.delete("1.0", 'end')
        self.precio_compra_entry.delete(0, 'end')
        self.precio_venta_entry.delete(0, 'end')
        self.stock_entry.delete(0, 'end')
        self.categoria_combobox.set("")
        self.unidad_combobox.set("")

    def generar_codigo_barras(self):
        """
        Genera un código único con prefijo 'JJ', fecha y un número aleatorio.
        Verifica que no exista ya en la base de datos local.
        """
        while True:
            codigo = "JJ" + datetime.now().strftime("%y%m%d%H%M%S%f") + str(random.randint(100, 999))
            
            if not self.db.existe_registro("productos", "codigo", codigo):
                return codigo
if __name__ == "__main__":
    
    root = ctk.CTk()
    ctk.set_appearance_mode("light")  # Opciones: "light", "dark", o "system"
    ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"
    gestor = GestorProductos(root, "", "1", "tienda_jfleong6_1.db")
    root.mainloop()
