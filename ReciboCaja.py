from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
import os
import tempfile

ruta_temporal = tempfile.gettempdir()
from num2words import num2words

def numero_a_letras(numero):
    letras = num2words(numero, lang='es')
    return letras.capitalize()  # Capitaliza la primera letra



def crearPDFReciboCaja(Datos,Orden,Ref):
    width, height = 80 * mm, 297 * mm  # Ancho de 80 mm y altura ajustada a A4
    ruta = os.path.join(ruta_temporal, f"GrupoJJ\\recibo-caja\\recibo-caja-{Ref}.pdf")
    c = canvas.Canvas(ruta, pagesize=(width, height))

    # Establecer tamaño de letra y margen
    c.setFont("Helvetica", 12)
    margen_izquierdo = 1
    margen_derecho = width - 5
    margen_superior = height - 10
    margen_inferior = 10
    y_pos = margen_superior - 10

    # Función para dibujar texto con márgenes
    def dibujar_texto(texto, x, y):
        c.drawString(x, y, texto)

    # Función para dibujar líneas separadoras
    def dibujar_linea(x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
    #Crear datos para la tabla
    letrasValor = numero_a_letras(Orden[-1])
    precio = '$ {:,}'.format(Orden[-1])
    datosOrdinarios =[[f"{Datos['Empresa']}"],
                      [""],
                      [f"Recibo de caja: N°: {Ref}"],
                      [f"Ciudad: {Datos["Ciudad"]}-{Datos["Departamento"]}"],
                      [f"Fecha: {Orden[2]}"],
                      [f"Recibo de: {Orden[4]}"],
                      [f"Documento: {Orden[3]}"],
                      [f"Habitaciones: {Orden[-4]}"],
                      [f"Total: {precio}"],
                      ["La suma de (En letras)"],
                      [letrasValor],
                      ["Por concepto de"]]
    
    estilos = [('SPAN', (0, 0), (0, 1)),
               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
               ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
               ('VALIGN', (0, 0), (-1, 1), 'MIDDLE'),
               ('FONTNAME', (0, 0), (-1, 1), 'Times-Bold'),
               ('FONTNAME', (0, 5), (-1, 6), 'Times-Bold'),
               ('FONTNAME', (0, 11), (-1, 11), 'Times-Bold'),
               ('LINEBELOW', (0, 7), (-1, 7), 1, colors.black),
               ('LINEBELOW', (0, 11), (-1, 11), 1, colors.black),
               ('FONTSIZE', (0, 0), (-1, 1), 15)]
              
    listaServicios = Orden[-5].split(',')
    for servicios in listaServicios:
        datosOrdinarios.append([servicios])
    estilos.append(('LINEBELOW', (0, len(datosOrdinarios)-1), (-1, len(datosOrdinarios)-1), 1, colors.black),)
    datosOrdinarios.append(["Efectivo $ {:,}".format(Orden[-3])])
    datosOrdinarios.append(["Transferencia $ {:,}".format(Orden[-2])])
    total_width = margen_derecho - margen_izquierdo
    cant_width = total_width * 0.1
    subcant_width = cant_width
    categoria_width = total_width * 0.5
    precio_width = total_width * 0.3

    # Estilo de la tabla
    #style = TableStyle(estilosProductos,hAlign='LEFT')
    
    style1 = TableStyle(estilos)
    
    
    tabla1 = Table(datosOrdinarios,colWidths=[width],hAlign='LEFT')
    tabla1.setStyle(style1)
    # Dibujar la tabla en el PDF
    tabla1.wrapOn(c, total_width, margen_superior)
    tabla1.drawOn(c, margen_izquierdo, margen_superior-tabla1._height)



    c.save()