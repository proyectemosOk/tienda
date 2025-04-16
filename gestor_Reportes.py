import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import filedialog
import pandas as pd
from conexion_base import ConexionBase
from tkcalendar import DateEntry

class SalesReportWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Reporte de Ventas")
        #self.window.geometry("1000x600")
        
        # Conesion a base de datos
        self.db = ConexionBase("tienda.db")

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        
        # Create filtro 
        self.create_filtro()
        # Create main metrics cards
        self.create_metric_cards()
        
        # Create charts frame
        self.create_charts_frame()

        # Create bar frame
        self.create_bar_frame()
        
        # Create products table
        self.create_products_table()
    
    def create_filtro(self):
        # Crear frame para los filtros
        filtro_frame = ctk.CTkFrame(self.window)
        filtro_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Filtro por Fecha (Desde - Hasta)
        ctk.CTkLabel(filtro_frame, text="Desde:").grid(row=0, column=0, padx=5)
        self.fecha_inicio = DateEntry(filtro_frame, locale="es_ES", date_pattern="yyyy-mm-dd", state="readonly", font = ("Arial",13))
        self.fecha_inicio.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(filtro_frame, text="Hasta:").grid(row=0, column=2, padx=5)
        self.fecha_fin = DateEntry(filtro_frame, locale="es_ES", date_pattern="yyyy-mm-dd", state="readonly", font = ("Arial",13))
        self.fecha_fin.grid(row=0, column=3, padx=5)

        # Filtro por Método de Pago
        ctk.CTkLabel(filtro_frame, text="Método de Pago:").grid(row=0, column=4, padx=5)
        self.metodo_pago = ctk.CTkComboBox(filtro_frame, values=["Todos", "Efectivo", "Transferencia", "CXC"])
        self.metodo_pago.grid(row=0, column=5, padx=5)
        
        # Botón para aplicar filtro
        aplicar_btn = ctk.CTkButton(filtro_frame, text="Aplicar Filtro", command=self.aplicar_filtro)
        aplicar_btn.grid(row=0, column=6, padx=10)

        # Final
        self.row = 1

    def aplicar_filtro(self):
        # Obtener valores de los filtros
        fecha_inicio = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        metodo_pago = self.metodo_pago.get()

        # Construcción de la consulta SQL dinámica
        query = """
            SELECT metodo_pago, SUM(valor) 
            FROM pagos_venta 
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND fecha >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND fecha <= ?"
            params.append(fecha_fin)
        if metodo_pago and metodo_pago != "Todos":
            query += " AND metodo_pago = ?"
            params.append(metodo_pago)

        query += " GROUP BY metodo_pago ORDER BY SUM(valor) ASC"

        # Ejecutar consulta con filtros aplicados
        resultados = self.db.ejecutar_personalizado(query, params)

        # Actualizar gráficos y reportes con los datos filtrados
        self.update_charts(resultados)
    def update_charts(self, resultados):
        # Limpiar el frame de gráficos antes de actualizar
        for widget in self.charts_frame.winfo_children():
            widget.destroy()

        # Crear un nuevo gráfico de pagos con los datos filtrados
        fig_donut = Figure(figsize=(3, 3))
        ax_donut = fig_donut.add_subplot(111)

        if resultados:
            payment_types, values = zip(*resultados)
        else:
            payment_types, values = [], []

        colors = ['#87CEEB', '#FFA07A', '#98FB98', '#FFD700', '#FF6347'][:len(payment_types)]

        ax_donut.pie(values, labels=payment_types, colors=colors, autopct='%1.1f%%',
                    wedgeprops=dict(width=0.5))
        ax_donut.set_title('Tipos de pagos (Filtrado)')

        canvas_donut = FigureCanvasTkAgg(fig_donut, master=self.charts_frame)
        canvas_donut.draw()
        canvas_donut.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Actualizar otros gráficos (Opcional)
        self.create_bar_frame()

    def create_metric_cards(self):
        # Obtención de datos desde la base de datos
        ventas_resultado = self.db.ejecutar_personalizado("""
            SELECT SUM(total_venta) AS total_ventas, 
                SUM(total_utilidad) AS total_utilidad, 
                SUM(total_compra) AS total_compras 
            FROM ventas
        """)[0]  # Obtenemos el primer resultado
        gastos_resultado = self.db.ejecutar_personalizado("""
            SELECT SUM(monto) AS total_gastos FROM gastos
        """)[0]  # Obtenemos el primer resultado

        total_ventas = ventas_resultado[0] or 0
        total_utilidad = ventas_resultado[1] or 0
        total_compras = ventas_resultado[2] or 0
        total_gastos = gastos_resultado[0] or 0

        # Crear un frame para las métricas
        metrics_frame = ctk.CTkFrame(self.window)
        metrics_frame.grid(row = self.row, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Ventas
        self.create_card(metrics_frame, 0, "Ventas", f"${total_ventas:,.2f}", "#1E90FF")

        # Utilidad
        self.create_card(metrics_frame, 1, "Utilidad", f"${total_utilidad:,.2f}", "#FF1493")

        # Compras
        self.create_card(metrics_frame, 2, "Compras", f"${total_compras:,.2f}", "#32CD32")

        # Gastos
        self.create_card(metrics_frame, 3, "Gastos", f"${total_gastos:,.2f}", "#FF8C00")

    def create_card(self, parent, column, title, value, color):
        """Crea una tarjeta para una métrica específica"""
        card = ctk.CTkFrame(parent, fg_color=color)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(card, text=title, font=("Arial", 20, "bold"), text_color="white").pack(pady=(10, 5))
        ctk.CTkLabel(card, text=value, font=("Arial", 24, "bold"), text_color="white").pack(pady=(5, 10))
 
    def create_charts_frame(self):
        self.charts_frame = ctk.CTkFrame(self.window)
        self.charts_frame.grid(row = self.row + 1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Create payment types donut chart
        fig_donut = Figure(figsize=(3,3))
        ax_donut = fig_donut.add_subplot(111)
 
        # Ejecutar consulta
        resultados = self.db.ejecutar_personalizado("""SELECT metodo_pago, SUM(valor) 
                                                    FROM pagos_venta 
                                                    GROUP BY metodo_pago 
                                                    ORDER BY SUM(valor) ASC""")

        # Separar en dos listas
        if len(resultados) > 0:
            if len(resultados) == 1:
                payment_types, values = zip(*[(resultados[0][0], resultados[0][1])])  # For single-element case
            else:
                payment_types, values = zip(*resultados)
        else:
            payment_types, values = [], []  # Handle case with no data
        colors = ['#87CEEB', '#FFA07A', '#98FB98', '#FFD700', '#FF6347'][:len(payment_types)]

        ax_donut.pie(values, colors=colors, autopct='%1.1f%%',
                    wedgeprops=dict(width=0.5))
        # Agregar la leyenda debajo del gráfico
        ax_donut.legend(payment_types, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=3)
        ax_donut.set_title('Tipos de pagos')
        
        canvas_donut = FigureCanvasTkAgg(fig_donut, master=self.charts_frame)
        canvas_donut.draw()
        canvas_donut.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
    
    def create_bar_frame(self):
        # Create bar chart
        fig_bar = Figure(figsize=(8,3))
        ax_bar = fig_bar.add_subplot(111)
        
        # Sample data for bar chart
        categories = ['Categoría 1', 'Categoría 2', 'Categoría 3']
        series_data = [4.3, 2.4, 2.0]
        bar_colors = ['#4682B4', '#6A5ACD', '#7B68EE']
        
        ax_bar.bar(categories, series_data, color=bar_colors)
        ax_bar.set_title('Ventas por categoría')
        ax_bar.set_ylabel('Ingresos ($)')
        
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=self.charts_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        
    def create_products_table(self):
        table_frame = ctk.CTkFrame(self.window)
        table_frame.grid(row=self.row + 1, column=2, padx=5, pady=5, sticky="nsew")
        
        # Table header
        ctk.CTkLabel(table_frame, text="Top 10 productos más vendidos",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Table headers
        headers_frame = ctk.CTkFrame(table_frame)
        headers_frame.pack(fill="x", padx=10)
        
        ctk.CTkLabel(headers_frame, text="Id", width=50).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(headers_frame, text="Producto", width=150).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(headers_frame, text="Cant", width=50).grid(row=0, column=2, padx=5)
        
        # Consulta SQL
        resultados = self.db.ejecutar_personalizado("""
            SELECT p.id, p.nombre, SUM(dv.cantidad) AS total_cantidad
            FROM detalles_ventas dv
            INNER JOIN productos p ON dv.producto_id = p.id
            GROUP BY p.id, p.nombre
            ORDER BY total_cantidad DESC
            LIMIT 10
        """)

        # Iteración para llenar la tabla
        for i, (producto_id, nombre, cantidad) in enumerate(resultados):
            row_frame = ctk.CTkFrame(table_frame)
            row_frame.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(row_frame, text=str(i+1), width=50).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(row_frame, text=nombre, width=150).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(row_frame, text=str(cantidad), width=50).grid(row=0, column=2, padx=5)

    def export_to_excel(self):
        # Dummy data for export
        data = {
            "Id": list(range(1, 11)),
            "Producto": [f"Producto {i+1}" for i in range(10)],
            "Cantidad": [(10-i)*10 for i in range(10)]
        }
        df = pd.DataFrame(data)
        
        # Save file dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesReportWindow(root)
    root.mainloop()
