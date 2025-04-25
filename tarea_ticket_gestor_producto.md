
# 🛠️ Tarea de Actualización - `ticket.py` y `gestor_Productos.py`

## 👤 Asignado a: @Jesús

## 📄 Descripción General

Esta tarea incluye actualizaciones en los archivos `ticket.py` y `gestor_Productos.py` para mejorar la funcionalidad de la interfaz de usuario y la interacción con las ventanas emergentes.

---

## ✅ **Objetivos:**

### 1. 🔄 **En `ticket.py`:**

#### a. **Botón "Nuevo" cambiar por "Cliente"**
   - Cambiar el texto del botón "Nuevo" por "Cliente".
   
#### b. **Letra de búsqueda de cliente**
   - Reducir el tamaño de la letra del campo de búsqueda de cliente.
   - Hacer que la búsqueda funcione por **nombre** y **cédula**, con sensibilidad para **mayúsculas y minúsculas**.
   - Ejemplo de código para hacerlo:
   ```python
   def filtrar_clientes(self, event):
       entrada = self.cliente_combo.get().lower()
       clientes_filtrados = [cliente for cliente in self.obtener_clientes() if entrada in cliente.lower()]
       self.cliente_combo.configure(values=clientes_filtrados)
   ```

#### c. **Ventana de "Nuevo Cliente"**
   - Asegurar que la ventana emergente de "Nuevo Cliente" siempre esté en primer plano cuando se invoque.
   ```python
   def nuevo_cliente(self):
       NuevoCliente(self.parent_frame)  # Ventana emergente de nuevo cliente
   ```

### 2. 📦 **En `gestor_Productos.py`:**

#### a. **Ventana para símbolo de unidad**
   - El cuadro de diálogo `simpledialog.askstring` para ingresar el símbolo de la unidad debe aparecer correctamente en primer plano y no quedar pegado o cubierto por otros elementos.
   - Asegurarse de que la ventana de entrada de símbolo sea visible y no quede detrás de otros elementos.
   
   **Acción:** En el código actual, el método para agregar la unidad muestra el símbolo de unidad detrás de otras ventanas, lo cual se debe corregir asegurándose de que la ventana sea emergente y visible.
   ```python
   simbolo = simpledialog.askstring("Nueva Unidad", f"Ingresa el símbolo para la unidad '{unidad}':")
   ```

---

## 🧠 **Recomendaciones Finales**

- **Para `ticket.py`:** Asegúrate de que los campos de cliente y el evento de búsqueda estén funcionando correctamente con la sensibilidad a mayúsculas y minúsculas.
- **Para `gestor_Productos.py`:** Verifica la visibilidad del `simpledialog.askstring` para que no se quede detrás de otros elementos.

---

## 🚀 **Implementación** 

Después de realizar los cambios, asegúrate de realizar pruebas en la interfaz para verificar que los botones y cuadros de entrada estén funcionando como se espera, especialmente en lo referente a la visibilidad y el orden de las ventanas emergentes.
