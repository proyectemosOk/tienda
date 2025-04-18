import sqlite3
from firebase_config import *
class ConexionBase:
    def __init__(self, nombre_bd):
        """
        Inicializa la conexión a la base de datos.
        """
        self.nombre_bd = nombre_bd
        self.firebase = ServicioFirebase("../proyectemosok-31150-firebase-adminsdk-fbsvc-fdae62578b.json")

    def conectar(self):
        """
        Establece y devuelve la conexión a la base de datos.
        """
        return sqlite3.connect(self.nombre_bd)

    def ejecutar_consulta(self, consulta, parametros=()):
        """
        Ejecuta una consulta genérica en la base de datos.
        Retorna el ID generado si es un INSERT, o None en otros casos.
        """
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(consulta, parametros)
            conexion.commit()
            
            # Detectamos si es una inserción y devolvemos el ID
            if consulta.strip().upper().startswith("INSERT"):
                return cursor.lastrowid
            else:
                return None

        except sqlite3.Error as e:
            print(f"❌ Error al ejecutar la consulta: \n{consulta}\n{e}")
            return None
        finally:
            conexion.close()


    def insertar(self, tabla, datos):
        """
        Inserta datos en la tabla especificada.
        tabla: str - Nombre de la tabla.
        datos: dict - Diccionario con los nombres de columnas y valores a insertar.
        """
        columnas = ", ".join(datos.keys())
        
        valores = tuple(datos.values())

        placeholders = ", ".join("?" for _ in datos)

        consulta = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        id_generado = self.ejecutar_consulta(consulta, valores)
        # --- Subir a Firebase si corresponde ---
        if self.firebase and id_generado:
            datos_con_id = datos.copy()
            datos_con_id["id"] = id_generado
            self.firebase.db.collection(tabla).document(str(id_generado)).set(datos_con_id)
            print(f"🔥 Documento '{id_generado}' insertado en colección '{tabla}' de Firebase.")

    
    def existe_registro(self, tabla, columna, valor):
        resultado = self.seleccionar(tabla, columnas=columna, condicion=f"{columna} = ?", parametros=(valor,))
        return len(resultado) > 0
    
    def seleccionar(self, tabla, columnas="*", condicion=None, parametros=()):
        """
        Selecciona datos de la tabla.
        tabla: str - Nombre de la tabla.
        columnas: str - Columnas a seleccionar, por defecto '*'.
        condicion: str - Condición WHERE opcional.
        parametros: tuple - Parámetros para la condición.
        """
        consulta = f"SELECT {columnas} FROM {tabla}"
        if condicion:
            consulta += f" WHERE {condicion}"
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(consulta, parametros)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar SELECT: {e}")
            return []
        finally:
            conexion.close()

    def actualizar(self, tabla, datos, condicion, parametros_condicion):
        """
        Actualiza datos en la tabla local y sincroniza con Firebase si corresponde.
        """
        asignaciones = ", ".join(f"{col} = ?" for col in datos.keys())
        valores = tuple(datos.values())
        consulta = f"UPDATE {tabla} SET {asignaciones} WHERE {condicion}"
        self.ejecutar_consulta(consulta, valores + parametros_condicion)

        # --- Sincronizar con Firebase ---
        if self.firebase:
            # Suponemos que la condición es algo como: "id = ?"
            # y que el primer parámetro en parametros_condicion es el ID del documento
            doc_id = str(parametros_condicion[0])
            try:
                self.firebase.db.collection(tabla).document(doc_id).update(datos)
                print(f"🔁 Documento '{doc_id}' actualizado en colección '{tabla}' de Firebase.")
            except Exception as e:
                print(f"❌ Error al actualizar en Firebase: {tabla}: {e}")

    def eliminar(self, tabla, condicion, parametros=()):
        """
        Elimina registros de la tabla según la condición.
        tabla: str - Nombre de la tabla.
        condicion: str - Condición WHERE.
        parametros: tuple - Parámetros para la condición.
        """
        consulta = f"DELETE FROM {tabla} WHERE {condicion}"
        self.ejecutar_consulta(consulta, parametros)

    def contar(self, tabla, condicion=None, parametros=()):
        """
        Cuenta registros en la tabla.
        tabla: str - Nombre de la tabla.
        condicion: str - Condición WHERE opcional.
        parametros: tuple - Parámetros para la condición.
        """
        consulta = f"SELECT COUNT(*) FROM {tabla}"
        if condicion:
            consulta += f" WHERE {condicion}"
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(consulta, parametros)
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar registros: {e}")
            return None
        finally:
            conexion.close()

    def ejecutar_personalizado(self, consulta, parametros=()):
        """
        Ejecuta una consulta personalizada y devuelve el resultado.
        consulta: str - Consulta SQL.
        parametros: tuple - Parámetros para la consulta.
        """
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            
            cursor.execute(consulta, parametros)

            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta personalizada: {e}")
            return None
        finally:
            conexion.commit()
            conexion.close()

    def existe_registro(self, tabla, columna, valor):
        """
        Verifica si existe un registro en la tabla, usando el método ejecutar_personalizado.
        Retorna True si existe al menos un resultado.
        """
        consulta = f"SELECT 1 FROM {tabla} WHERE {columna} = ? LIMIT 1"
        resultado = self.ejecutar_personalizado(consulta, (valor,))
        return bool(resultado)

