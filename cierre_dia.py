import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from imprimir import Imprimir
from datetime import datetime
import os

class CerrarDia(tk.Toplevel):
    def __init__(self, master, db):
        
        self.db = db
        self.imprimir = Imprimir()
        # Consulta para obtener datos de ventas y pagos
        consulta = """
            SELECT v.id, v.total_venta, p.metodo_pago, SUM(p.valor) AS total_pago
            FROM ventas v
            LEFT JOIN pagos_venta p ON v.id = p.venta_id
            WHERE v.estado = 1
            GROUP BY v.id, p.metodo_pago
            ORDER BY v.id, p.metodo_pago
        """
        ventas_y_pagos = self.db.ejecutar_personalizado(consulta)
        print(ventas_y_pagos)
        if ventas_y_pagos == []:
            messagebox.showerror("Día vacío", "No se pudieron obtener los datos.")
            return
        super().__init__(master)
        
        # Configuración de la ventana
        self.title("Cierre de Día")
        
        # Crear marco principal
        frame_principal = ttk.Frame(self, padding=10)
        frame_principal.grid(row=0, column=0, sticky="nsew")
        
        # Treeview para listar ventas
        ttk.Label(frame_principal, text="Ventas del Día", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=(0, 10))
        self.tabla = ttk.Treeview(frame_principal, columns=("ID", "Total Compra"), show="headings", height=10)
        self.tabla.heading("ID", text="ID Venta")
        self.tabla.heading("Total Compra", text="Total Compra")
        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Total Compra", width=150, anchor="center")
        self.tabla.grid(row=1, column=0, padx=10, pady=10)
        
        # Inicializar totales
        self.total_ventas = 0
        self.pagos_por_metodo = {"Efectivo": 0, "CXC": 0, "Transferencia": 0}
        
        # Procesar los resultados de ventas y pagos
        id = ""
        for venta_id, total_venta, metodo_pago, valor in ventas_y_pagos:
            print(valor)
            if id != venta_id:
                self.tabla.insert('', 'end', values=[venta_id, self.formatear_pesos(total_venta)])
                self.total_ventas += total_venta
                id = venta_id
            if metodo_pago:
                self.pagos_por_metodo[metodo_pago] += valor
                
            
        # Mostrar resumen de pagos
        ttk.Label(frame_principal, text="Resumen de Pagos", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=(10, 5))
        frame_resumen = ttk.Frame(frame_principal)
        frame_resumen.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        for metodo, total_pago in self.pagos_por_metodo.items():
            ttk.Label(frame_resumen, text=f"{metodo}: {self.formatear_pesos(total_pago)}", font=("Arial", 10)).pack(anchor="w")
        
        # Botón para guardar en .txt
        ttk.Button(self, text="Guardar Resumen", command=self.guardar_resumen).grid(row=1, column=0, pady=10)
        
        # Mostrar el total de ventas
        ttk.Label(self, text=f"Total de Ventas: {self.formatear_pesos(self.total_ventas)}", font=("Arial", 12, "bold")).grid(row=2, column=0, pady=(5, 10))
    
    def formatear_pesos(self, valor):
        """Formato para valores monetarios."""
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def guardar_resumen(self):
        if not os.path.exists('tickets'):
            os.makedirs('tickets')
        
        # Nombre de archivo con fecha y hora
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        n_factura = self.db.seleccionar("cierre_dia", "MAX(ID)")[0][0]
        if n_factura is None:
            n_factura = 0
        nombre_archivo = f"tickets\\cierre_dia_{n_factura}.txt"
        
        
        with open(nombre_archivo, "w") as f:
            f.write("Resumen del Día\n")
            f.write("-"*27 + "\n")
            f.write(f"Fecha: {fecha_actual}\n")
            f.write(f"N°: {n_factura}\n")
            f.write(f"{'ID':<5}{'VENTA':<22}\n")
            f.write("-" * 27 + "\n")
            lista_id_ventas = []
            for item in self.tabla.get_children():
                venta_id, total_compra = self.tabla.item(item, "values")
                lista_id_ventas.append(venta_id)
                f.write(f"{venta_id:<5}{total_compra:<22}\n")
            f.write("\nResumen de Pagos\n")
            f.write("-"*27 + "\n")
            efectivo =0
            Transferencia =0
            cxc = 0
            for metodo, total_pago in self.pagos_por_metodo.items():
                if total_pago>0:
                    if metodo =="Efectivo":
                        efectivo = total_pago
                    if metodo =="Transferencia":
                        Transferencia = total_pago
                    if metodo =="CXC":
                        cxc = total_pago
                    f.write(f"{metodo}: {self.formatear_pesos(total_pago)}\n")
            f.write(f"Total: {self.total_ventas}\n")
            
        self.imprimir.imprimir_archivo(nombre_archivo)
        self.db.ejecutar_personalizado("UPDATE ventas SET estado = 0")
        self.db.insertar("cierre_dia",{
                        "fecha_entrada": fecha_actual,             
                        "ids_ventas": ",".join(lista_id_ventas),
                        "monto": self.total_ventas   
        })
        self.db.insertar("entregas_diarias", {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "efectivo": efectivo,
            "transferencias": Transferencia,
            "cxc": cxc,
            "total": self.total_ventas,
            "estado":1
            })
        self.destroy()
