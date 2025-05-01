import customtkinter as ctk
from conexion_base import ConexionBase

class FormularioProducto:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        
        # Frame principal
        self.form_frame = ctk.CTkFrame(self.master)
        self.form_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Fuentes
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
        self.stock_entry = ctk.CTkEntry(self.form_frame, font=font_entry, state="disabled")
        self.stock_entry.grid(row=0, column=5, padx=5, pady=(2, 3))
        
        # Precio de compra
        ctk.CTkLabel(self.form_frame, text="Precio de compra:", font=font_label).grid(row=1, column=0, padx=5, pady=(2, 3))
        self.precio_compra_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.precio_compra_entry.grid(row=1, column=1, padx=5, pady=(2, 3))
        
        # Precio de venta
        ctk.CTkLabel(self.form_frame, text="Precio de venta:", font=font_label).grid(row=1, column=2, padx=5, pady=(2, 3))
        self.precio_venta_entry = ctk.CTkEntry(self.form_frame, font=font_entry)
        self.precio_venta_entry.grid(row=1, column=3, padx=5, pady=(2, 3))
        
        # Categoría (ComboBox)
        ctk.CTkLabel(self.form_frame, text="Categoría:", font=font_label).grid(row=2, column=0, padx=5, pady=(2, 3))
        self.categoria_combobox = ctk.CTkComboBox(self.form_frame, values=[])
        self.categoria_combobox.grid(row=2, column=1, padx=5, pady=(2, 3))
       
        # Unidad (ComboBox)
        ctk.CTkLabel(self.form_frame, text="Unidad:", font=font_label).grid(row=2, column=2, padx=5, pady=(2, 3))
        self.unidad_combobox = ctk.CTkComboBox(self.form_frame, values=[])
        self.unidad_combobox.grid(row=2, column=3, padx=5, pady=(2, 3))
        
        # Descripción (Textbox)
        ctk.CTkLabel(self.form_frame, text="Descripción:", font=font_label).grid(row=1, column=4, padx=5, pady=(2, 3), sticky="w")
        self.descripcion_entry = ctk.CTkTextbox(self.form_frame, font=font_entry, height=50)
        self.descripcion_entry.grid(row=2, column=4, padx=5, pady=(2, 3), rowspan=2, columnspan=2, sticky="news")
        
        # Botones
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Botón Agregar
        self.agregar_btn = ctk.CTkButton(
            self.btn_frame,
            text="Agregar",
            command=self.agregar_producto,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.agregar_btn.grid(row=0, column=0, padx=5)
        
        # Cargar datos iniciales
        self._cargar()
    
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
            self.unidad_combobox.set(lista_unidades[2])  # Opcional: valor por defecto
    
    def agregar_producto(self):
        """Aquí irá la lógica para agregar un nuevo producto a la base de datos."""
        # Más adelante se puede implementar
        pass

if __name__ == "__main__":
    

    # Inicializar la app
    root = ctk.CTk()
    root.title("Formulario de Producto")

    # Crear conexión a base de datos
    db = ConexionBase("tienda_jfleong6_1.db")  # ← Cambia el nombre del archivo de la base de datos

    # Crear formulario
    def actualizar_dummy():
        pass  # Función vacía de prueba

    formulario = FormularioProducto(root, db)

    root.mainloop()