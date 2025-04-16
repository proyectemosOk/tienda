import sqlite3
import random
from datetime import datetime, timedelta
# Función para conectar a la base de datos
def conectar_bd(nombre_bd):
    return sqlite3.connect(nombre_bd)

# Función para crear las tablas
def crear_tablas():
    conexion = conectar_bd("tienda.db")
    cursor = conexion.cursor()

        # Crea la tabla de datos de la empresa
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datos (
        dato TEXT UNIQUE,  -- UNIQUE para evitar duplicados
        descripcion TEXT
    )
    ''')

    # Inserta datos por defecto en la tabla 'datos' si no existen
    datos = [
        ("Empresa", "Grupo JJ"),
        ("Celular", "3175414049"),
        ("Dirección", "Calle 13 # 25 - 14"),
        ("Correo", "grupojj@gmail.com"),
        ("Pagina Web", "www.grupojj.com")
    ]

    for dato in datos:
        cursor.execute('''
        INSERT OR IGNORE INTO datos (dato, descripcion) VALUES (?, ?)
        ''', dato)

    # Crea la tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,  -- UNIQUE para evitar duplicados
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('admin', 'usuario'))
    )
    ''')

    # Inserta un usuarios por defecto si no existe
    usuarios = [('Admin', '4dm1n321', 'admin'),
                ('ventas', 'ventas123', 'usuario')
    ]
    for dato in usuarios:
        cursor.execute('''
        INSERT OR IGNORE INTO usuarios (id, nombre, contrasena, rol) VALUES (Null, ?, ?, ?)
        ''', dato)


    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL unique,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio_compra REAL,
        precio_venta REAL,
        stock INTEGER,
        categoria TEXT NOT NULL,
        unidad TEXT NOT NULL
    )
    ''')
    productos = [
    (1,1,"Laptop", "Laptop básica para oficina",1200000, 1500000, 10, "Tecnología", "Unidad"),
    (2,2,"Mouse", "Mouse inalámbrico",20000, 25000, 50, "Tecnología", "Unidad"),
    (3,3,"Teclado", "Teclado mecánico retroiluminado",55000, 75000, 30, "Tecnología", "Unidad"),
    (4,4,"Silla Gamer", "Silla ergonómica para juegos",2000000, 2500000, 5, "Muebles", "Unidad"),
    (5,5,"Escritorio", "Escritorio de madera para oficina",6000000, 750000, 10, "Muebles", "Unidad"),
    (6,6,"Camiseta", "Camiseta de algodón, talla M",100000, 15000, 100, "Ropa", "Unidad"),
    (7,7,"Zapatos", "Zapatos deportivos, talla 42",35000, 50000, 20, "Calzado", "Unidad"),
    (8,8,"Smartphone", "Teléfono inteligente de última generación",60000, 80000, 15, "Tecnología", "Unidad"),
    (9,9,"Audífonos", "Audífonos con cancelación de ruido",80000, 120000, 25, "Tecnología", "Unidad"),
    (10,10,"Mochila", "Mochila resistente al agua",20000, 45000, 20, "Accesorios", "Unidad")
    ]

    #cursor.executemany('''INSERT OR IGNORE INTO productos (id, codigo, nombre, descripcion, precio_compra, precio_venta, stock, categoria, unidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', productos)

    # Crear tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_document TEXT NOT NULL, 
            numero TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        )
    ''')

    # Inserta un cliente por defecto si no existe
    cursor.execute(
        "INSERT OR IGNORE INTO clientes (id, nombre, tipo_document, numero, telefono, email) VALUES(?, ?, ?, ?, ?, ?)", 
        (1, "Varios", "Cedula", "1", "1", "1")
    )


    # Crear tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendedor_id TEXT NOT NULL,
        cliente_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        total_venta REAL NOT NULL,
        total_compra REAL,
        total_utilidad REAL,
        estado INTEGER DEFAULT 1,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (vendedor_id) REFERENCES usuarios (id)
    )
    ''')

    # Crear tabla de detalles de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalles_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        estado INTEGER DEFAULT 1,
        FOREIGN KEY (venta_id) REFERENCES ventas (id),
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unidad text NOT NULL UNIQUE,
        simbolo text
    )
    ''')
    productos = [
    (1,"Unidad","Und"),
    (2,"Gramos","g"),
    (3,"MiliLitros","mL"),
    ]
    for producto in productos:
        cursor.execute('''INSERT OR IGNORE INTO unidades (id, unidad, simbolo) VALUES (?, ?, ?)
        ''', producto)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria text NOT NULL UNIQUE
    )
    ''')
    
    categorias = [
    (1,"Tecnología"),
    (2,"Muebles"),
    (3,"Ropa"),
    (4, "Calzado"),
    (5, "Accesorios")
    ]
    #cursor.executemany('''INSERT OR IGNORE INTO categorias (id, categoria) VALUES (?, ?)''', categorias)


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagos_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        metodo_pago TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER,
                cantidad INTEGER,
                fecha DATETIME,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                usuario TEXT NOT NULL,
                observacion TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
                FOREIGN KEY (usuario) REFERENCES usuarios (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_modificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_producto INTEGER NOT NULL,         
            id_usuario INTEGER NOT NULL,          
            fecha_hora TEXT NOT NULL,             
            detalle TEXT                         
        )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lotes_productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_compra REAL NOT NULL,
    fecha_ingreso DATE NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id)
        )
    ''')

    productos = [
    (1,1, 10, 1200000, "2025-01-09"),
    (2,2, 50, 20000, "2025-01-09"),
    (3,3, 30, 55000, "2025-01-09"),
    (4,4, 5, 2000000, "2025-01-09"),
    (5,5, 10, 6000000, "2025-01-09"),
    (6,6, 100, 100000, "2025-01-09"),
    (7,7, 20, 35000, "2025-01-09"),
    (8,8, 15, 60000, "2025-01-09"),
    (9,9, 25, 80000, "2025-01-09"),
    (10,10, 20, 20000, "2025-01-09")]

    #cursor.executemany('''INSERT OR IGNORE INTO lotes_productos (id, id_producto, cantidad, precio_compra, fecha_ingreso) VALUES (?, ?, ?, ?, ?)''', productos)
        
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS compra_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER NOT NULL,
    id_lote integer not null,
    precio_compra REAL NOT NULL,
    FOREIGN KEY (id_lote) REFERENCES lotes_productos(id),
    FOREIGN KEY (id_venta) REFERENCES ventas(id)
        )
    ''')
    # Proveedores
    # Tabla de Proveedores
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        rut TEXT UNIQUE,
        direccion TEXT,
        telefono TEXT,
        email TEXT,
        fecha_registro DATE DEFAULT CURRENT_DATE,
        estado INTEGER DEFAULT 1  -- 1 activo, 0 inactivo
        )
    ''')

    # Corregir la sentencia INSERT
    cursor.execute(
    "INSERT OR IGNORE INTO proveedores (id, codigo, nombre, rut, direccion, telefono, email) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    (1, "1", "Varios", "1", "1", "1", "1")
)


    # Tabla de Facturas de Proveedor
    cursor.execute('''CREATE TABLE IF NOT EXISTS facturas_proveedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_factura TEXT NOT NULL,
        proveedor_id INTEGER,
        fecha_emision DATE NOT NULL,
        fecha_vencimiento DATE,
        "tipo_pago" TEXT,
        monto_total INTEGER NOT NULL,
        monto_pagado INTEGER DEFAULT 0,
        estado_pago TEXT DEFAULT 'PENDIENTE', -- PENDIENTE, PARCIAL, PAGADO
        usuario_id TEXT,
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )
    ''')
    # Tabla de Pagos de Factura
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagos_factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER,
        tipo_pago_id INTEGER,
        fecha_pago DATE NOT NULL,
        monto DECIMAL(10,2) NOT NULL,
        observaciones TEXT,
        FOREIGN KEY (factura_id) REFERENCES facturas_proveedor(id),
        FOREIGN KEY (tipo_pago_id) REFERENCES tipos_pago(id)
        )
    ''')
    # Tabla de Detalle de Entrada por Proveedor
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER NOT NULL,
        precio_compra DECIMAL(10,2) NOT NULL,
        precio_venta DECIMAL(10,2) NOT NULL,
        fecha_entrada DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (factura_id) REFERENCES facturas_proveedor(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''') 
    
    # Tabla de Tipos de Pago
    cursor.execute('''CREATE TABLE IF NOT EXISTS tipos_pago (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')
    cursor.executemany("INSERT OR IGNORE INTO tipos_pago (id, nombre, descripcion) VALUES (?, ?, ?)", 
((1,'EFECTIVO', 'Pago en efectivo'),
(2,'TRANSFERENCIA', 'Transferencia bancaria'),
(3,'TARGETA', 'Pago con tarjeta de débito')
))
    
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_entrada DATE DEFAULT CURRENT_DATE,
            monto REAL NOT NULL,
            descripcion TEXT NOT NULL,
            metodo_pago TEXT NOT NULL
        )
    ''')
    # Confirmar los cambios y cerrar la conexión
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cierre_dia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_entrada DATE DEFAULT CURRENT_DATE,
            ids_ventas NOT NULL,
            monto REAL NOT NULL
        )
    ''')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregas_diarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            efectivo INTEGER DEFAULT 0,
            transferencias INTEGER DEFAULT 0,
            cxc INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0,
            estado INTEGER DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cierre_inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            total_venta INTEGER DEFAULT 0,
            total_entregado INTEGER DEFAULT 0,
            faltante INTEGER DEFAULT 0
        )
    """)
    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

    
if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas exitosamente.")

    
