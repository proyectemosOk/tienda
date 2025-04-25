
# 🛠️ Tarea de Mejora - `tienda.py` con `ConexionBase`

## 👤 Asignado a: @Sebastián

## 📄 Descripción General

Esta tarea tiene como objetivo corregir y optimizar la visualización y búsqueda de productos en la pantalla de la tienda. A continuación, se detallan las acciones que debes realizar.

---

## ✅ Objetivos

### 1. 🔍 Corregir motor de búsqueda
   - La funcionalidad de búsqueda no está respondiendo correctamente.
   - Se debe permitir buscar productos por código, ID, descripción y nombre.
   - Capturar el evento de `Enter` para realizar la búsqueda automáticamente.

   Ejemplo de código:
   ```python
   def actulizar_productos(self, event=None):
       buscar = self.codigo_producto_entry_buscar.get()
       lista = self.db.seleccionar("productos", "id, nombre, precio_venta, stock, descripcion", "stock > 0")
       if buscar != "":
           self.lista_productos_ver = self.filtrar(buscar, lista)
       else:
           self.lista_productos_ver = lista

       self.actulizar_interfaz_productos()
   ```

### 2. 📊 Mostrar productos más vendidos
   - Al cargar la interfaz, mostrar los productos más vendidos primero.
   - Consultar los datos de la base de datos para obtener los más vendidos, basados en la venta acumulada (`detalle_factura`, `cantidad`).
   
   Consulta SQL sugerida:
   ```python
   productos_mas_vendidos = self.db.ejecutar_personalizado(
       '''
       SELECT p.id, p.nombre, p.precio_venta, p.stock, p.descripcion
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

### 3. 🖼️ Ajustar visualización en columnas
   - Hacer que la visualización se adapte al ancho disponible.
   - Calcular dinámicamente el número de columnas necesarias basándose en el ancho del contenedor.

   Ejemplo de código para distribuir las columnas:
   ```python
   ancho_contenedor = self.ver_frame_productos.winfo_width() or self.ver_frame_productos.winfo_reqwidth()
   ancho_tarjeta = 250  # valor estimado

   # Cálculo automático del número de columnas
   columnas = max(1, ancho_contenedor // ancho_tarjeta)

   # Configurar columnas dinámicas
   for col in range(columnas):
       self.ver_frame_productos.columnconfigure(col, weight=1)

   # Colocar productos en las columnas
   for i, producto in enumerate(lista):
       fila = i // columnas
       columna = i % columnas
       tarjeta = VistaProductos(self.ver_frame_productos, producto, self.img_productos, self.ticket)
       tarjeta.frame_producto.grid(row=fila, column=columna, padx=10, pady=5, sticky="nsew")
   ```

---

## 🧠 **Recomendaciones Finales**

- Verificar que los productos más vendidos se muestren correctamente en la vista inicial.
- Asegurarse de que las columnas se ajusten dinámicamente según el ancho del contenedor, y los productos se distribuyan adecuadamente en la interfaz.
- Probar con diferentes tamaños de ventana para asegurar que la interfaz responda correctamente.

---

## 🚀 **Implementación** 

Después de realizar los cambios, asegúrate de realizar pruebas en la interfaz para verificar que los botones, cuadros de búsqueda y las visualizaciones se ajusten según lo esperado, especialmente en lo referente a la visibilidad y la adaptación al ancho de la ventana.
