
# Guía de Actualización para `gestor_Entadas.py`

Esta guía está diseñada para facilitar a un nuevo desarrollador la implementación de ciertas mejoras en la interfaz y funcionalidad del módulo `GestorEntradas`, que forma parte del sistema de gestión de entradas de productos por proveedor.

## ✅ Requisitos de Modificación

### 1. Buscar Proveedor por CC, Nombre o Teléfono con la tecla Enter

**Ubicación:** Método `buscar_proveedor` y campo `self.proveedor_entry`

**Acciones:**
- Asociar el evento `<Return>` al campo de entrada de proveedor:
```python
self.proveedor_entry.bind("<Return>", lambda e: self.buscar_proveedor())
```
- Modificar el método `buscar_proveedor` para incluir búsqueda por teléfono:
```python
proveedor = self.db.seleccionar(
    "proveedores", "*",
    "codigo = ? OR nombre = ? OR telefono = ?",
    (codigo, codigo, codigo,)
)
```

---

### 2. Mejorar la Interfaz de Ingreso de Nuevo Cliente

**Ubicación:** Método `mostrar_toplevel_proveedor`

**Sugerencias:**
- Usar `sticky="ew"` en los `grid()` para que los `Entry` se ajusten.
- Validaciones visuales o mensajes en caso de errores.
- Colocar los `Label` y `Entry` en una distribución clara.

---

### 3. Agregar campo de búsqueda de productos por múltiples atributos

**Ubicación:** Método `_crear_frame_productos`

**Acciones:**
- Añadir nuevo campo de búsqueda y botón (o evento enter):
```python
self.buscar_multi_entry = ctk.CTkEntry(row1, width=200, placeholder_text="Buscar por código, nombre...")
self.buscar_multi_entry.pack(side="left", padx=5)
self.buscar_multi_entry.bind('<Return>', self.buscar_producto_multicampo)
```
- Crear método `buscar_producto_multicampo`:
```python
def buscar_producto_multicampo(self, event=None):
    busqueda = self.buscar_multi_entry.get().strip()
    producto = self.db.seleccionar(
        "productos", "*",
        "codigo = ? OR nombre LIKE ? OR descripcion LIKE ?",
        (busqueda, f"%{busqueda}%", f"%{busqueda}%")
    )
    ...
```

- Si no existe el producto, mostrar formulario para registrar uno nuevo.

---

### 4. Cerrar la ventana al guardar la factura

**Ubicación:** Método `finalizar_entrada`

**Estado Actual:**
- Ya implementado con `self.destroy()` al final del método, no requiere cambios.

---

## 🧭 Estructura del Código

- **Clase Principal:** `GestorEntradas(tk.Toplevel)`
- **Componentes Clave:**
  - `_crear_frame_busqueda()` → Entrada de proveedor
  - `_crear_frame_factura()` → Datos de factura
  - `_crear_frame_productos()` → Ingreso de producto
  - `_crear_tabla_productos()` → Tabla + botón finalizar
- **Base de datos:** Usando `ConexionBase`, con métodos `seleccionar`, `insertar`, `ejecutar_personalizado`.
- **Ventanas adicionales:** Se gestionan con `CTkToplevel`.

---

## 📌 Notas Finales

Este archivo guía está diseñado para facilitar modificaciones específicas sin perder de vista la estructura del código y la lógica actual del sistema.
