import os
from datetime import datetime
from imprimir import Imprimir
import time 
class GeneradorTicket:
    def __init__(self, datos_empresa):
        """
        Inicializa el generador de tickets
        
        :param datos_empresa: Diccionario con información de la empresa
        Ejemplo:
        {
            'nombre': 'Mi Negocio',
            'direccion': 'Calle Principal 127',
            'telefono': '555-1274',
            'rfc': 'XAXX010101000'
        }
        """
        self.datos_empresa = datos_empresa
    
    def generar_ticket(self, items, n_factura, total_venta, cliente="varios", CXC = "No"):
        print(items)

        """
        Genera un archivo de ticket de compra
        
        :param items: Lista de items vendidos
        :param total_venta: Total de la venta
        :param cliente: Nombre del cliente (opcional)
        """
        # Crear directorio de tickets si no existe
        if not os.path.exists('tickets'):
            os.makedirs('tickets')
        
        # Nombre de archivo con fecha y hora
        fecha_actual = datetime.now()
        if CXC =="Si":
            nombre_archivo = f"tickets\\ticket_{n_factura}_cxc.txt"
        else:
            nombre_archivo = f"tickets\\ticket_{n_factura}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            # Encabezado de la empresa
            for dato in self.datos_empresa:
                if self.datos_empresa[dato] not in "":
                    f.write(self._centrar(self.datos_empresa[dato], 27) + "\n")
            
            # Información de la venta
            f.write(f"N°: {n_factura}\n")
            f.write(f"Fecha: {fecha_actual.strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Cliente: {cliente}\n")
            f.write("-" * 27 + "\n")
            
            # Encabezados de columnas
            f.write(f"{'Cod':<5}{'Prod':<10}{'Cant':<5}{'Total':<6}\n")
            f.write("-" * 27 + "\n")
            
            # Detalles de los items
            for item in items:
                f.write(
                    f"{item['id']:<5}"
                    f"{item['nombre'][:10]:<10}"
                    f" {item['cantidad']:<5}"
                    f"{self.formatear_pesos(item['total_precio']):<6}\n"
                )
            
            f.write("-" * 27 + "\n")
            
            # Total de la venta
            f.write(f"Total:{'':>7}{self.formatear_pesos(total_venta)}\n")
            if CXC =="Si":
                f.write(f"Cuenta de cobro CXC\n")
            
            # Pie de ticket
            f.write("\n")
            f.write(self._centrar("¡Gracias por su compra!", 27) + "\n")
            f.write(self._centrar("Ticket generado", 27) + "\n")
        
        return nombre_archivo
    
    def formatear_pesos(self, valor):
        return f"$ {valor:,.0f}".replace(",", ".")
    
    def _centrar(self, texto, ancho):
        """
        Centra un texto en un ancho específico
        
        :param texto: Texto a centrar
        :param ancho: Ancho total
        :return: Texto centrado
        """
        return texto.center(ancho)

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de datos de empresa
    datos_empresa = {
        'nombre': 'Mi Tienda',
        'direccion': 'Av. Principal 127',
        'telefono': '555-1274',
        'rfc': 'XAXX010101000'
    }
    
    # Ejemplo de items
    items_ejemplo = [
        {
            'id': '001',
            'nombre': 'Producto5421 A',
            'cantidad': 2,
            'precio': 10.50,
            'total_precio': 21.00
        },
        {
            'id': '002',
            'nombre': 'Producto B',
            'cantidad': 1,
            'precio': 15.75,
            'total_precio': 15.75
        }
    ]
    # 
    imprimir = Imprimir()
    # Generar ticket
    generador = GeneradorTicket(datos_empresa)
    archivo_ticket = generador.generar_ticket(items_ejemplo,5, 36.75)
    imprimir.imprimir_archivo(archivo_ticket)
    print(f"Ticket generado: {archivo_ticket}")