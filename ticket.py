import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from cargar_iconos import cargar_iconos
from item import Item
from generar_ticket import GeneradorTicket
from conexion_base import ConexionBase
from imprimir import Imprimir
from agregarScroll import AgregarScrollVerticar
from nuevo_cliente import NuevoCliente
# Registrar la venta
from datetime import datetime

class TicketDeVenta:
    def __init__(self, parent_frame, usuario, iconos,actulizar_productos):
        self.parent_frame = parent_frame
        self.items = {}  # Diccionario para almacenar items en el formato {id: {"nombre": ..., "precio": ..., "cantidad": ...}}
        self.total = 0
        self.iconos = iconos
        self.actulizar_productos = actulizar_productos
        self.usuario = usuario
        self.db = ConexionBase("tienda.db")
        self.datos = {i[0]:i[1] for i in self.db.seleccionar("datos","*")}
        self.generador_ticket = GeneradorTicket(self.datos)
        self.imprimir = Imprimir()
        # Encabezado de la lista
        self.header_frame = ctk.CTkFrame(self.parent_frame, corner_radius=10)

        # Contenedor para los items
        self.items_frame_1 = tk.Frame(self.parent_frame)
        frame_agregar_productos = AgregarScrollVerticar(self.items_frame_1)
        frame_agregar_productos.frame.config(bg="white")
        self.items_frame = tk.Frame(frame_agregar_productos.frame)
        self.items_frame.config(bg="white")
        #self.items_frame = ctk.CTkFrame(items_frame, corner_radius=20,  fg_color="white")

        # Nuevo frame para tipos de pago
        self.payment_frame = ctk.CTkFrame(self.parent_frame, corner_radius=15)

        # Footer con total y botones
        self.footer_frame = ctk.CTkFrame(self.parent_frame, corner_radius=12)

        self.header_frame.pack(fill="x")
        self.items_frame_1.pack(fill="both",expand=True)
        self.items_frame.pack(fill="both", expand = True, anchor = "n")
        self.payment_frame.pack(fill="x", ipadx = 3, pady=10)
        self.footer_frame.pack(fill="x", ipady=10)

        
        self.cliente_combo = ctk.CTkComboBox(
            self.header_frame, 
            width=15,
            values=self.obtener_clientes(), 
            corner_radius=50, 
            font=("Arial", 25),
            justify="left"
        )
        self.cliente_combo.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        self.cliente_combo.set("")  # Valor inicial vacío

        # Agregar un evento para actualizar la lista mientras se escribe
        self.cliente_combo.bind("<KeyRelease>", self.filtrar_clientes)
        
        
        self.nuevo_cliente_button = ctk.CTkButton(self.header_frame, text="Nuevo", font = ("Arial", 25), command=self.nuevo_cliente)
        self.nuevo_cliente_button.pack(side="left", padx=5)

        self.vender_button = ctk.CTkButton(self.footer_frame, text="Vender", font = ("Arial", 25), fg_color="#1bdf00", text_color="white", command=self.vender)
        self.vender_button.pack(side="left", padx=10)

        self.total_label = ctk.CTkLabel(self.footer_frame, text="$0", font=("Arial", 30, "bold"))
        self.total_label.pack(side="right", padx=10)


        # Definir métodos de pago
        self.metodos_pago = {
            "Efectivo":{"color": "#4CAF50", "comando": self.seleccionar_efectivo},
            "Transferencia": {"color": "#FF9800", "comando": self.seleccionar_transferencia},
            "CXC": {"color": "#2196F3", "comando": self.seleccionar_tarjeta}            
        }

        # Variable para rastrear el método de pago seleccionado
        self.metodo_pago_var = ctk.StringVar(value="")

        # Crear botones de pago
        for metodo in self.metodos_pago:
            frame = ctk.CTkFrame(self.payment_frame)
            frame.pack(side="left",pady = 10)
            boton = ctk.CTkButton(
                frame, 
                text=metodo,
                corner_radius=50,
                font=("Arial", 12),
                fg_color=self.metodos_pago[metodo]["color"],
                hover_color=self.oscurecer_color(self.metodos_pago[metodo]["color"]),
                command=self.metodos_pago[metodo]["comando"]
            )
            self.metodos_pago[metodo]["entry"] = ctk.CTkEntry(frame, 
                                                              corner_radius=50, 
                                                              placeholder_text=self.total,
                                                              font = ("Arial", 12))            
            boton.pack(padx=5,pady=5,ipady=5, expand=True)
    
    def obtener_clientes(self):
        """
        Obtiene la lista de nombres de los clientes desde la base de datos.
        """
        clientes = self.db.seleccionar("clientes", "nombre")
        return [cliente[0] for cliente in clientes] if clientes else []

    def filtrar_clientes(self, event):
        """
        Filtra las opciones de clientes en función de la entrada del usuario
        y muestra la lista desplegable.
        """
        entrada = self.cliente_combo.get().lower()
        clientes_filtrados = [cliente for cliente in self.obtener_clientes() if entrada in cliente.lower()]
        self.cliente_combo.configure(values=clientes_filtrados)

        # Forzar la apertura de la lista desplegable si hay resultados
        if clientes_filtrados:
            self.cliente_combo.event_generate("<Button-1>")

    def nuevo_cliente(self):
        # Acción al crear un nuevo cliente (puedes implementar la lógica aquí)
        NuevoCliente(self.parent_frame)

    def agregar_item(self, id_producto, nombre, precio,stock,icono):
        
        if id_producto in self.items:
            # Si ya existe el producto, incrementamos la cantidad
            self.items[id_producto].sumar()

        else:
            # Si no existe, lo añadimos
            self.items[id_producto] = Item(self.items_frame,id_producto, nombre, precio,stock, self.actulizar_total, self.eliminar_item, icono)
            self.actulizar_total()
    
    def actulizar_total(self):
        # Actualizar total
        self.total = sum(self.items[data].total_precio for data in self.items)
        
        self.total_label.configure(text=self.formatear_pesos(self.total))
    
    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def eliminar_item(self, id_producto):
        # Eliminar un item del ticket
        if id_producto in self.items:
            del self.items[id_producto]
            self.actulizar_total()

    def vender(self):
        # Obtener o registrar cliente
        nombre_cliente = self.cliente_combo.get() if self.cliente_combo.get() != "" else "Varios"
        cliente_id = None
        
        if nombre_cliente != "Varios":
            # Buscar si el cliente ya existe
            cliente_existente = self.db.seleccionar("clientes", "*", "nombre = ?", (nombre_cliente,))
            cliente_id = cliente_existente[0][0]

        else:
            # Para ventas a "Varios", usar un ID específico o crear un cliente genérico
            cliente_varios = self.db.seleccionar("clientes", "*", "nombre = ?", ("Varios",))
            cliente_id = cliente_varios[0][0]

        
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar la venta
        self.db.insertar("ventas", {
            "vendedor_id": self.usuario,
            "cliente_id": cliente_id,
            "fecha": fecha_actual,
            "total_venta": self.total,
            "total_compra":0,
            "total_utilidad":0,
            "estado":1
        })
        
        # Obtener el ID de la venta recién creada
        venta_nueva = self.db.seleccionar("ventas", "*", "fecha = ? AND cliente_id = ?", (fecha_actual, cliente_id,))
        if venta_nueva == []:
            venta_id = 0
        else:
            venta_id = venta_nueva[-1][0]  # Tomamos el último en caso de que haya múltiples en el mismo segundo

        # Registrar los detalles de la venta
        total_compra = 0
        items = []
        for item_id, item in self.items.items():
            items.append({
            'id': item.id,
            'nombre': item.nombre,
            'cantidad': item.cantidad,
            'precio': item.precio_actual,
            'total_precio': item.total_precio
        })
            
            self.db.insertar("detalles_ventas", {
                "venta_id": venta_id,
                "producto_id": item.id,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_actual
            })
            
            nuevo_stock = int(item.stock) - int(item.cantidad)
            
            #self.db.actualizar("productos",{"stock": nuevo_stock},"id = ?",(int(item.id),))
            self.db.ejecutar_consulta(f"UPDATE productos SET stock = {nuevo_stock} WHERE codigo = {item.id}")

            total_compra += self.registrar_lotes(venta_id,item.id,int(item.cantidad))
            
        # Registrar los pagos (ahora sin validación previa de método)
        pagos_realizados = self.registrar_pagos(venta_id)
        
        # Actulizar total compra y total utilidad
        self.db.actualizar("ventas",{"total_utilidad":self.total-total_compra},"id = ?",(venta_id,))
        self.db.actualizar("ventas",{"total_compra":total_compra},"id = ?",(venta_id,))
        
        # Generar e imprimir el ticket
        archivo = self.generador_ticket.generar_ticket(items, str(venta_id), self.total, nombre_cliente)
        self.imprimir.imprimir_archivo(archivo,"80mm Series Printer")
        print(pagos_realizados)
        if "CXC" in pagos_realizados:
            archivo = self.generador_ticket.generar_ticket(items, str(venta_id), self.total, nombre_cliente, CXC ="Si")
            self.imprimir.imprimir_archivo(archivo,"80mm Series Printer")
        
        
        # Limpiar el ticket después de la venta
        self.limpiar_ticket()
        
    def registrar_lotes(self,id_venta, id_producto, cantidad_solicitada):
        # Obtener lotes disponibles para el producto, ordenados por fecha
        lotes = self.db.seleccionar("lotes_productos","id, cantidad, precio_compra", "id_producto = ? ORDER BY fecha_ingreso ASC",(id_producto,))

        cantidad_restante = int(cantidad_solicitada)
        total_precio = 0

        for lote in lotes:
            id_lote, cantidad_lote, precio_compra = lote
            
            
            if cantidad_restante <= 0:
                break

            if cantidad_lote <= cantidad_restante:
                # Usar todo el lote
                compra = int(cantidad_lote) * int(precio_compra)
                total_precio += compra
                
                cantidad_restante -= cantidad_lote
                self.db.eliminar("lotes_productos","id = ?",(id_lote,))
                
            else:
                # Usar parte del lote
                compra = cantidad_restante * precio_compra
                total_precio += compra
                
                self.db.ejecutar_consulta("UPDATE lotes_productos SET cantidad = cantidad - ? WHERE id = ?", (cantidad_restante, id_lote,))
                
                cantidad_restante = 0
            self.db.insertar("compra_venta",{"id_venta":id_venta,"id_lote":id_lote,"precio_compra":compra})

        
        return total_precio

    def registrar_pagos(self, venta_id):
        """
        Registra los pagos asociados a una venta. Si no hay método seleccionado,
        asume que el pago es en efectivo por el total.
        """
        pagos_realizados = {}
        total_pagado = 0

        # Verificar si hay algún método de pago seleccionado y visible
        algun_pago_seleccionado = False
        for metodo, datos in self.metodos_pago.items():
            entry = datos.get('entry')
            if entry and entry.winfo_ismapped() and entry.get().strip():
                algun_pago_seleccionado = True
                break

        # Si no hay ningún método seleccionado, asumir efectivo por el total
        if not algun_pago_seleccionado:
            self.db.insertar("pagos_venta", {
                "venta_id": venta_id,
                "metodo_pago": "Efectivo",
                "valor": self.total
            })
            return [{"Efectivo":self.total}]

        # Si hay métodos seleccionados, procesar cada uno
        for metodo, datos in self.metodos_pago.items():
            entry = datos.get('entry')
            if entry and entry.winfo_ismapped():  # Verificar si la entrada está visible
                valor_texto = entry.get().strip()
                if valor_texto:  # Si hay un valor ingresado
                    try:
                        valor = float(valor_texto.replace('$', '').replace(',', '').replace('.', ''))
                        if valor > 0:
                            self.db.insertar("pagos_venta", {
                                "venta_id": venta_id,
                                "metodo_pago": metodo,
                                "valor": valor
                            })
                            pagos_realizados[metodo]= valor
                            total_pagado += valor
                            # Limpiar el campo después de registrar
                            entry.delete(0, 'end')
                    except ValueError:
                        print(f"Error al procesar el pago con {metodo}")
        
        # Verificar si los pagos cubren el total
        if abs(total_pagado - self.total) > 0:  # Usar una pequeña tolerancia para decimales
            raise ValueError(f"El total pagado (${total_pagado:,.2f}) no coincide con el total de la venta (${self.total:,.2f})")
        efectivo,Transferencia,cxc = [0,0,0]
        if "Efectivo" in pagos_realizados:
            efectivo =  pagos_realizados["Efectivo"]
        if "Transferencia" in pagos_realizados:
            Transferencia =  pagos_realizados["Transferencia"]
        if "CXC" in pagos_realizados:
            cxc =  pagos_realizados["CXC"]

        self.db.insertar("entregas_diarias", {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Efectivo": efectivo,
            "transferencias": Transferencia,
            "cxc": cxc,
            "total": self.total,
            "estado":1
            })
        return pagos_realizados
    
    def limpiar_ticket(self):
        """
        Limpia todos los elementos del ticket después de una venta
        """
        
        
        # Limpiar el campo de cliente
        self.cliente_combo.set("")
        
        # Resetear el total
        self.total = 0
        self.total_label.configure(text=self.formatear_pesos(0))
        
        # Limpiar método de pago si existe
        if hasattr(self, 'metodo_pago_var'):
            self.metodo_pago_var.set("")
            # Ocultar todas las entradas de pago
            for metodo in self.metodos_pago.values():
                if 'entry' in metodo:
                    metodo['entry'].pack_forget()
        # Limpiar los items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.items.clear()
        self.actulizar_productos()
    
    def oscurecer_color(self, color_hex, factor=0.8):
        """Oscurece un color hex para el efecto hover."""
        r = int(int(color_hex[1:3], 16) * factor)
        g = int(int(color_hex[3:5], 16) * factor)
        b = int(int(color_hex[5:7], 16) * factor)
        return f'#{r:02x}{g:02x}{b:02x}'

    def seleccionar_efectivo(self):
        self.metodo_pago_var.set("Efectivo")
        self.metodos_pago["Efectivo"]["entry"].pack(padx=10, pady=10, fill="x", expand=True)

    def seleccionar_tarjeta(self):
        self.metodo_pago_var.set("CXC")
        self.metodos_pago["CXC"]["entry"].pack(padx=10, pady=10, fill="x", expand=True)

    def seleccionar_transferencia(self):
        self.metodo_pago_var.set("Transferencia")
        self.metodos_pago["Transferencia"]["entry"].pack(padx=10, pady=10, fill="x", expand=True)
