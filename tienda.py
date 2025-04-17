import tkinter as tk
from tkinter import ttk, messagebox
from conexion_base import ConexionBase
import crear_bd
import customtkinter as ctk
from cargar_iconos import cargar_iconos
from agregarScroll import AgregarScrollVerticar
from VistaProductos import VistaProductos
from ticket import TicketDeVenta
from gestor_Productos import GestorProductos
from gestor_Entadas import GestorEntradas
from datos_empresa import DatosApp
from conexion_base import ConexionBase
from gestor_gasto import GestorDeGastos
from gestor_cirerre_inventario import GestorCierreInventario
from cierre_dia import CerrarDia
from entregas_diaria import EntregaDiaria
import time
class InterfazPrincipal:
    def __init__(self, master, menu, ventanda_principal):
        """
        fondo = #008ADF
        """
        self.style = ttk.Style()
        # Crear barra de menú
        self.menu_barra = menu
        self.style.configure('principal.TButton', font=('Helvetica', 12), anchor='w')
        self.style.configure('titulo.TLabel', font=('Helvetica', 30),foreground = "white", background="#008ADF")
        self.style.configure('producto.TLabel', font=('times', 20),foreground = "white", background="#008ADF", wraplength=150)
        self.style.configure('descripcion.TLabel', font=('times', 15),foreground = "white", background="#008ADF", wraplength=150)
        self.style.configure('precio.TLabel', font=('times', 25),foreground = "#1bdf00", background="#008ADF")
        self.style.configure('background.TFrame', background="#008ADF")
        self.master = master
        self.master_principal = ventanda_principal

        self.ancho_pantalla = self.master.winfo_screenwidth() 
        self.alto_pantalla = self.master.winfo_screenheight()

        self.menu_principal = ventanda_principal
        
        self.iconos = cargar_iconos()
        # Establecer el ícono de la ventana usando PIL para cargar la imagen
       
        self.img_productos = cargar_iconos("img_productos")
        ctk.set_appearance_mode("light")  # Opciones: "light", "dark", o "system"
        ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"
        # Base de datos
        crear_bd.crear_tablas()
        self.db = ConexionBase("tienda.db")
        self.interfaz_ventas("1")
        self.master.bind_all('<F5>',self.actulizar_productos)

    def interfaz_ventas(self, usuario):
        self.usuario = usuario
        self.crear_menu()
        self.frame_pedido = tk.Frame(self.master,bg="white")
        self.frame_pedido.pack(fill="both",expand=True)
        frame_productos = tk.Frame(self.frame_pedido,bg="white")
        self.frame_ticket = tk.Frame(self.frame_pedido,bg="white")
        # Opcional: Establecer tamaño fijo
        self.frame_ticket.pack_propagate(False)
        frame_productos.configure(width=self.ancho_pantalla*0.78)
        self.frame_ticket.configure(width=self.ancho_pantalla*0.22)
        frame_productos.pack(side="left", expand=True, fill="both")
        self.frame_ticket.pack(side="right", fill="y")

        self.ticket = TicketDeVenta(self.frame_ticket, self.usuario, self.iconos, self.actulizar_productos)
        
        frame_buscar_productos = tk.Frame(frame_productos,bg="white")
        frame_ver_productos = tk.Frame(frame_productos,bg="white")        

        frame_buscar_productos.pack(fill="x")
        frame_ver_productos.pack(fill="both",expand=True)

        self.producto_buscar_var = tk.StringVar()
        self.codigo_producto_entry_buscar = ctk.CTkEntry(frame_buscar_productos, placeholder_text="Buscar producto")
        self.codigo_producto_entry_buscar.pack(fill="x",expand=True,padx=5,pady=5)
        self.codigo_producto_entry_buscar.bind('<Return>', self.actulizar_productos)


        scroll_productos = AgregarScrollVerticar(frame_ver_productos, bg_color="white")
        frame_productos = scroll_productos.get_frame()

        # Ahora usa frame_productos para agregar tus VistaProductos
        #self.ver_frame_productos = frame_productos
        self.ver_frame_productos = tk.Frame(frame_productos,bg="white")
        self.ver_frame_productos.pack(fill='both',expand = 1)
        self.actulizar_productos()
        
    def actulizar_interfaz_productos (self):
        self.limpiar_frame(self.ver_frame_productos)
        
        if len(self.lista_productos_ver)>50:
            lista = self.lista_productos_ver[0:50]
        else:
            lista = self.lista_productos_ver
        print(len(lista))
        inicio = time.time()
        for i, producto in enumerate(lista):
            # Calcular posición en la cuadrícula
            fila = int(i) // 5
            columna = int(i) % 5
            x = VistaProductos(self.ver_frame_productos, producto, self.img_productos, self.ticket)
            x.frame_producto.grid(row=fila, column=columna, padx=10, pady=5,ipadx=2, ipady =3, sticky="nesw")
        print(f"Tiempo transcurrido: {time.time() - inicio:.2f} segundos")
                    
    def limpiar_frame(self, frame):
        # Destruye todos los widgets hijos del frame
        for widget in frame.winfo_children():
            widget.destroy()
    
    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")

    def crear_menu(self):
        
        
        # Menú empresa
        menu_empresa = tk.Menu(self.master_principal, tearoff=0) 
        menu_empresa.add_command(label="Actulizar datos", compound="left", command=self.datos_empresa)
        self.menu_barra.add_cascade(label="Empresa", menu=menu_empresa)

        # Menú Inventario
        menu_inventario = tk.Menu(self.menu_barra, tearoff=0)
        menu_inventario.add_command(label="Gestor de Productos", compound="left", command=self.gestor_productos)
        menu_inventario.add_command(label="Gestor de Entradas", compound="left", command=self.gestor_entradas)
        menu_inventario.add_command(label="Gestor de gastos", compound="left", command=self.gestor_gastos)
        menu_inventario.add_command(label="Cierre de Inventario", compound="left", command=self.cierre_inventario)
        menu_inventario.add_command(label="Cierre de día", compound="left", command=self.cerrar_dia)
        menu_inventario.add_command(label="Entrega del día", compound="left", command=self.entrega_diaria)
        
        self.menu_barra.add_cascade(label="Inventario", menu=menu_inventario)

        # Menú Acerca de
        menu_acerca_de = tk.Menu(self.menu_barra, tearoff=0)
        menu_acerca_de.add_command(label="Acerca de la aplicación", compound="left", command=self.acerca_de)
        self.menu_barra.add_cascade(label="Acerca de", menu=menu_acerca_de)

        # Configurar la barra de menú en la ventana principal
        self.master_principal.config(menu=self.menu_barra)

    def cerrar_dia(self):
        CerrarDia(self.master,self.db)
    
    def entrega_diaria(self):
        EntregaDiaria(self.master,self.db)
    
    def datos_empresa(self):
        DatosApp(self.master)
    
    def gestor_productos(self):

        GestorProductos(self.master, self.actulizar_productos, self.usuario)

    def gestor_entradas(self):
        GestorEntradas(self.master, self.actulizar_productos, self.usuario)
    
    def gestor_gastos(self):
        GestorDeGastos(self.master)        
    
    def cierre_inventario(self):
        GestorCierreInventario(self.master, self.db)

    def acerca_de(self):
        # Método para mostrar información de la aplicación
        messagebox.showinfo("Acerca de", "Esta es una aplicación de gestión para la tienda.\nDesarrollado por Grupo JJ.")

    def actulizar_productos(self, event=None):
        self.img_productos = cargar_iconos("img_productos")
        buscar = self.codigo_producto_entry_buscar.get()
        lista = self.db.seleccionar("productos", "id, nombre, precio_venta, stock, descripcion, id", "stock > 0")
        print(buscar)
        if buscar != "":
            # Obtiene todos los productos de la base de datos
            # Filtra la lista de productos
            self.lista_productos_ver = self.filtrar(buscar, lista)
        else:
            # Si no hay búsqueda, muestra todos los productos
            self.lista_productos_ver = lista

        self.actulizar_interfaz_productos()

    def filtrar(self, buscar, lista):
        # Convierte el término de búsqueda a minúsculas para evitar problemas de mayúsculas/minúsculas
        buscar = buscar.lower()
        
        # Filtra la lista de productos
        filtrada = []
        for productos in lista:
            if buscar in productos[0].lower() or buscar in productos[1].lower():
                filtrada.append(productos)
        
        return filtrada
