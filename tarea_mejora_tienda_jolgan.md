
# 🛠️ Tarea de Mejora - `tienda.py`

## 👤 Asignado a: @Jolgan

## 📄 Descripción General

Esta tarea tiene como propósito mejorar la búsqueda de productos, mostrar los productos más vendidos por defecto y optimizar la disposición de las tarjetas en la vista principal de productos dentro del archivo `tienda.py`.

---

## ✅ Objetivos

### 1. 🔍 Mejorar Motor de Búsqueda

- **Archivo:** `tienda.py`
- **Método:** `filtrar()` y `actulizar_productos()`
- **Detalles:**
  - El motor actual solo busca por ID y nombre.
  - Debe ampliarse para incluir código, nombre, descripción e ID.
  - Capturar el evento `Enter` para ejecutar la búsqueda.

```python
def filtrar(self, buscar, lista):
    buscar = buscar.lower()
    filtrada = []
    for producto in lista:
        if any(buscar in str(p).lower() for p in (producto[0], producto[1], producto[4], producto[5])):
            filtrada.append(producto)
    return filtrada
```

---

### 2. 📊 Mostrar Productos Más Vendidos por Defecto

- **Comportamiento esperado:** cuando no hay término de búsqueda, mostrar los productos más vendidos.
- **Uso de base de datos (`ConexionBase`) con `self.db`:**

```python
productos_mas_vendidos = self.db.ejecutar_personalizado(
    '''
    SELECT p.id, p.nombre, p.precio_venta, p.stock, p.descripcion, p.id 
    FROM productos p
    JOIN (
        SELECT producto_id, SUM(cantidad) AS total_vendido
        FROM detalle_factura
        GROUP BY producto_id
        ORDER BY total_vendido DESC
        LIMIT 50
    ) d ON d.producto_id = p.id
    WHERE p.stock > 0
    '''
)
self.lista_productos_ver = productos_mas_vendidos
```

- **Ubicación:** dentro del método `actulizar_productos()` cuando `buscar == ""`.

---

### 3. 🖼️ Ajustar Visualización a Pantallas Adaptativas

- **Método:** `actulizar_interfaz_productos`
- **Objetivo:** Que el número de columnas de productos se **adapte automáticamente al ancho disponible del contenedor**, no una cantidad fija (como 5).

---

#### ✅ Lógica sugerida:

1. **Obtener el ancho del contenedor visible** (`self.ver_frame_productos`).
2. **Definir un ancho mínimo estimado por tarjeta**, por ejemplo, 250px.
3. **Calcular cuántas columnas caben**:

```python
ancho_contenedor = self.ver_frame_productos.winfo_width() or self.ver_frame_productos.winfo_reqwidth()
ancho_tarjeta = 250  # valor estimado para cada tarjeta
columnas = max(1, ancho_contenedor // ancho_tarjeta)
```

4. **Configurar las columnas dinámicamente**:

```python
for col in range(columnas):
    self.ver_frame_productos.columnconfigure(col, weight=1)
```

5. **Distribuir los productos en la cuadrícula según columnas calculadas**:

```python
for i, producto in enumerate(lista):
    fila = i // columnas
    columna = i % columnas
    tarjeta = VistaProductos(self.ver_frame_productos, producto, self.img_productos, self.ticket)
    tarjeta.frame_producto.grid(row=fila, column=columna, padx=10, pady=5, sticky="nsew")
```

---

✅ **Consejo adicional:**
Para asegurar que el ancho del contenedor ya esté calculado tras el renderizado de la ventana, puedes usar:

```python
self.after(100, self.actulizar_interfaz_productos)
```

Esto retrasa la ejecución ligeramente para asegurar que `winfo_width()` retorne un valor realista.

---
