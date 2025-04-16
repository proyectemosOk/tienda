import win32print
import win32api
import os
import logging

class Imprimir:
    def __init__(self, logger=None):
        """
        Inicializa la clase de impresión con soporte opcional de logging.
        
        Args:
            logger (logging.Logger, opcional): Logger para manejar mensajes de depuración

        """# Configurar logging básico
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logger or logging.getLogger(__name__)

    def validar_archivo(self, archivo):
        """
        Valida la existencia y accesibilidad del archivo.
        
        Args:
            archivo (str): Ruta del archivo a imprimir
        
        Returns:
            bool: True si el archivo existe y es legible, False en caso contrario
        """
        if not archivo or not isinstance(archivo, str):
            self.logger.error("Ruta de archivo inválida")
            return False
        
        if not os.path.exists(archivo):
            self.logger.error(f"El archivo no existe: {archivo}")
            return False
        
        if not os.access(archivo, os.R_OK):
            self.logger.error(f"No se tiene permiso de lectura para el archivo: {archivo}")
            return False
        
        return True

    def obtener_impresora(self, nombre_impresora):
        """
        Busca una impresora por nombre.
        
        Args:
            nombre_impresora (str): Nombre de la impresora a buscar
        
        Returns:
            str or None: Nombre completo de la impresora si se encuentra, None en caso contrario
        """
        try:
            impresoras = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL + win32print.PRINTER_ENUM_CONNECTIONS, 
                None, 
                1
            )
            
            impresora_encontrada = next(
                (printer[2] for printer in impresoras 
                 if nombre_impresora.lower() in printer[2].lower()), 
                None
            )
            
            return impresora_encontrada
        
        except Exception as e:
            self.logger.error(f"Error al buscar impresora: {e}")
            return None

    def imprimir_archivo(self, archivo, nombre_impresora=None):
        """
        Imprime un archivo en una impresora específica o predeterminada.
        
        Args:
            archivo (str): Ruta del archivo a imprimir
            nombre_impresora (str, opcional): Nombre de la impresora. Si no se especifica, usa la predeterminada
        
        Returns:
            bool: True si la impresión fue exitosa, False en caso contrario
        """
        if not self.validar_archivo(archivo):
            print("hola")
            return False

        impresora_original = None
        try:
            # Guardar la impresora predeterminada original
            impresora_original = win32print.GetDefaultPrinter()
            
            # Si se especifica nombre de impresora, intentar seleccionarla
            if nombre_impresora:
                impresora_target = self.obtener_impresora(nombre_impresora)
                
                if impresora_target:
                    win32print.SetDefaultPrinter(impresora_target)
                    self.logger.info(f"Imprimiendo en {impresora_target}")
                else:
                    self.logger.warning(f"Impresora {nombre_impresora} no encontrada. Usando impresora predeterminada.")
            
            # Imprimir archivo
            
            win32api.ShellExecute(0, "print", archivo, None, ".", 0)
            self.logger.info(f"Archivo {archivo} enviado a impresión")
            return True
        
        except Exception as e:
            self.logger.error(f"Error crítico al imprimir: {e}")
            return False
        
        finally:
            # Restaurar impresora original
            if impresora_original:
                win32print.SetDefaultPrinter(impresora_original)
