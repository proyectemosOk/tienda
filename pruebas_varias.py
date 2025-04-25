import sqlite3
import bcrypt

# Crear o conectar a la base de datos
conn = sqlite3.connect("test_users.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
)
""")

# Paso 1: Registro del usuario
usuario = "admin"
contrasena_original = "111"

# Generar hash y guardarlo
hash_guardado = bcrypt.hashpw(contrasena_original.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Insertar en la base de datos (evitar duplicado)
cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
if not cursor.fetchone():
    cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_guardado))
    conn.commit()
    print("✅ Usuario registrado con éxito.")
else:
    print("⚠️ Usuario ya registrado.")

# Paso 2: Simulación de login
contrasena_ingresada = input("Ingresa la contraseña para iniciar sesión: ")

# Buscar el usuario
cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
resultado = cursor.fetchall()

if resultado:
    hash_almacenado = resultado[0][0].encode('utf-8')
    if bcrypt.checkpw(contrasena_ingresada.encode('utf-8'), hash_almacenado):
        print("✅ Contraseña correcta. Bienvenido!")
    else:
        print("❌ Contraseña incorrecta.")
else:
    print("❌ Usuario no encontrado.")

conn.close()
