from firebase_config import ServicioFirebase
firebase = ServicioFirebase("../proyectemosok-31150-firebase-adminsdk-fbsvc-fdae62578b.json")


def cargar_tipos():
    tipos = [
        "PC", "Portátil", "Impresora", "Cámara", "DVR"
    ]
    for tipo in tipos:
        firebase.db.collection("tipos").document(tipo.lower()).set({
            "nombre": tipo
        })
    print("Tipos cargados correctamente.")

def cargar_servicios():
    servicios = [
        "Mantenimiento", "Actualización", "Reparación", "Actualizar Hardware"
    ]
    for servicio in servicios:
        firebase.db.collection("servicios").document(servicio.lower().replace(" ", "_")).set({
            "nombre": servicio
        })
    print("Servicios cargados correctamente.")

if __name__ == "__main__":
    cargar_tipos()
    cargar_servicios()
