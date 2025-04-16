from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generar_control_inventario(nombre_archivo, productos, max_columnas=9):
    """
    Genera un PDF con una tabla de productos donde las columnas 'ID' y 'Nombre' abarcan dos filas.

    :param nombre_archivo: Nombre del archivo PDF.
    :param productos: Lista de productos, cada producto es una lista [id, nombre].
    :param max_columnas: Número máximo de columnas adicionales para entradas y fechas.
    """
    # Configuración de página
    ancho_pagina, alto_pagina = landscape(letter)
    margen_izq = 20
    margen_sup = 2  # Reducción del margen superior

    # Definición de anchos de columna
    col_widths = [25, 200, 50]  # ID y Nombre
    num_columnas = max_columnas
    ancho_restante = ancho_pagina - margen_izq - sum(col_widths)
    ancho_col_extra = min(70, ancho_restante / num_columnas)
    col_widths += [ancho_col_extra] * num_columnas

    # Encabezados (fila 1 y fila 2)
    fila1 = ["ID", "Nombre", "Precio"] + [f"Entrada/Final" for i in range(num_columnas)]
    fila2 = ["", "", ""] + ["Fecha: YYYY/MM/DD" for _ in range(num_columnas)]

    # Datos de la tabla (agregar las columnas vacías para entradas y fechas)
    datos_tabla = [fila1, fila2]
    
    # Añadir los productos con las columnas adicionales vacías
    for producto in productos:
        x = list(producto)
        x[2] =f"$ {x[2]:,.0f}".replace(",", ".")
        if len(x[1])>38:
            x[1]=x[1][0:38]
        datos_tabla.append(x + [""] * num_columnas)  # Agregar columnas vacías para entradas y fechas

    # Crear el documento
    pdf = SimpleDocTemplate(nombre_archivo, pagesize=landscape(letter))

    # Crear la tabla
    tabla = Table(datos_tabla, colWidths=col_widths)

    # Estilo de la tabla
    estilo = TableStyle([
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente de la primera fila
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Tamaño de fuente
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Líneas de la tabla
        ('SPAN', (0, 0), (0, 1)),  # Combinar celdas de ID
        ('SPAN', (1, 0), (1, 1)),  # Combinar celdas de Nombre
        ('SPAN', (2, 0), (2, 1)),  # Combinar celdas de Precio
        ('FONTSIZE', (3, 0), (-1, 2), 5),
        ('ALIGN', (3, 0), (-1, 2), 'LEFT'),
        ('FONTSIZE', (0, 0), (2,1), 12),
        ('VALIGN', (0, 0), (2,1), 'MIDDLE'),
        ('VALIGN', (2, 0), (-1,1), 'MIDDLE'),
        ('TEXTCOLOR', (3, 0), (-1,1), "#B0B0B0"),
        ('WORDWRAP', (1, 2), (1, -1), True),
    ])
    tabla.setStyle(estilo)

    # Agregar contenido al PDF y generarlo
    pdf.build([tabla])
    print(f"El archivo '{nombre_archivo}' se ha generado correctamente.")

if __name__ == "__main__":
    # Datos de prueba
    productos = [
        [1, "Producto A"],  # Aquí solo tienes ID y Nombre, las columnas adicionales serán vacías
        [2, "Producdsssssssssssawwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwssssssssto B"],
        [3, "Producto C"],
        # Agrega más filas según sea necesario
    ]

    # Generar el PDF
    generar_control_inventario("tabla_productos_combinados.pdf", productos)
