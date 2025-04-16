import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import os
from imprimir import Imprimir

class EntregaDiaria(tk.Toplevel):
    def __init__(self, master, db=None):
        super().__init__(master)
        self.db = db
        self.title("Entrega Diaria de Valores")
        self.imprimir = Imprimir()
        
        # Variables para almacenar los valores
        self.efectivo_var = tk.StringVar(value="0")
        self.transferencias_var = tk.StringVar(value="0")
        self.cxc_var = tk.StringVar(value="0")
        self.total_var = tk.StringVar(value="$ 0")
        
        self.setup_ui()
        
        # Bind para actualizar el total cuando cambian los valores
        self.efectivo_var.trace_add("write", self.actualizar_total)
        self.transferencias_var.trace_add("write", self.actualizar_total)
        self.cxc_var.trace_add("write", self.actualizar_total)

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame, 
            text="Entrega de Valores", 
            font=("Arial", 24)
        )
        titulo.pack(pady=20)
        
        # Frame para los campos de entrada
        inputs_frame = ctk.CTkFrame(main_frame,bg_color="transparent")
        inputs_frame.pack(fill="x", padx=20, pady=10)
        
        # Efectivo
        self.crear_campo_entrada(
            inputs_frame,
            "Efectivo",
            self.efectivo_var,
            0
        )
        
        # Transferencias
        self.crear_campo_entrada(
            inputs_frame,
            "Transferencias",
            self.transferencias_var,
            1
        )
        
        # Cuentas por Cobrar
        self.crear_campo_entrada(
            inputs_frame,
            "Cuentas por Cobrar",
            self.cxc_var,
            2
        )
        
        # Total
        total_frame = ctk.CTkFrame(main_frame)
        total_frame.pack(fill="x", padx=20, pady=(20,10))
        
        ctk.CTkLabel(
            total_frame,
            text="Total:",
            font=("Arial", 20)
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            total_frame,
            textvariable=self.total_var,
            font=("Arial", 20)
        ).pack(side="right", padx=10)
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Guardar",
            command=self.guardar_entrega
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.destroy
        ).pack(side="right", padx=10)

    def crear_campo_entrada(self, parent, label_text, variable, row):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 16)
        ).pack(side="left", padx=10)
        
        entry = ctk.CTkEntry(
            frame,
            textvariable=variable,
            width=200,
            font=("Arial", 16)
        )
        entry.pack(side="right", padx=10)
        
        # Bind para validar entrada numérica
        entry.bind("<KeyRelease>", self.validar_numero)
        entry.bind("<FocusIn>", self.on_focus_in)

    def validar_numero(self, event):
        widget = event.widget
        valor = widget.get()
        
        # Eliminar caracteres no numéricos
        nuevo_valor = ''.join(c for c in valor if c.isdigit())
        
        if nuevo_valor != valor:
            widget.delete(0, tk.END)
            widget.insert(0, nuevo_valor)

    def on_focus_in(self, event):
        # Seleccionar todo el texto cuando se enfoca el campo
        event.widget.select_range(0, tk.END)
        event.widget.icursor(tk.END)

    def actualizar_total(self, *args):
        try:
            efectivo = int(self.efectivo_var.get() or 0)
            transferencias = int(self.transferencias_var.get() or 0)
            cxc = int(self.cxc_var.get() or 0)
            
            total = efectivo + transferencias + cxc
            self.total_var.set(f"$ {total:,.0f}".replace(",", "."))
        except ValueError:
            self.total_var.set("$ 0")

    def guardar_entrega(self):
        try:
            efectivo = int(self.efectivo_var.get() or 0)
            transferencias = int(self.transferencias_var.get() or 0)
            cxc = int(self.cxc_var.get() or 0)
            
            # Aquí añadirías la lógica para guardar en la base de datos
            fecha = datetime.now().strftime("%Y-%m-%d")
            # Ejemplo de guardado (ajusta según tu estructura de BD):
            cierre = {
                 "Efectivo": efectivo,
                 "Transferencias": transferencias,
                 "CXC": cxc,
                 "TOTAL": efectivo + transferencias + cxc
            }
            self.db.insertar("entregas_diarias", {"fecha": fecha, "Efectivo": efectivo,
                 "Transferencias": transferencias,
                 "CXC": cxc,
                 "TOTAL": efectivo + transferencias + cxc,
                 "ESTADO":1})
            self.guardar_resumen(cierre)
            
            messagebox.showinfo("Éxito", "Entrega guardada correctamente")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la entrega: {str(e)}")

    def formatear_pesos(self, valor):
        """Formato para valores monetarios."""
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def guardar_resumen(self,cierre):
        if not os.path.exists('tickets'):
            os.makedirs('tickets')
        
        # Nombre de archivo con fecha y hora
        n_factura = self.db.seleccionar("entregas_diarias", "MAX(ID)")[0][0]
        if n_factura is None:
            n_factura = 0
        nombre_archivo = f"tickets\\entrega_diaria{n_factura}.txt"
        
        
        with open(nombre_archivo, "w") as f:
            f.write("Entrega del Día\n")
            f.write("-"*27 + "\n")
            f.write(f"Fecha: {datetime.now().strftime("%Y-%m-%d")}\n")
            f.write(f"N°: {n_factura}\n")
            f.write(f"{'Medio':<14}{'Total':<13}\n")
            f.write("-" * 27 + "\n")

            for item in cierre:
                if int(cierre[item])>0:
                    f.write(f"{item:<14}{cierre[item]:<13}\n")
            f.write("-"*27 + "\n")


        self.imprimir.imprimir_archivo(nombre_archivo)
  
        self.destroy()