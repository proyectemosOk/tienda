from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from conexion_base import *
from orden import Orden
from firebase_config import ServicioFirebase
from datetime import datetime
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

conn_db = ConexionBase("tienda.db")
firebase = conn_db.firebase

@app.route('/')
def index():
    return render_template('orden.html')

@app.route('/orden')
def orden():
    return render_template('orden.html')

@app.route('/submit', methods=['POST'])
def submit():
    form = request.form

    # Procesar TIPO
    tipo = form['tipo']
    if tipo == "__nuevo__":
        tipo = form['nuevo_tipo'].strip()
        if tipo and not conn_db.existe_registro("tipos", "nombre", tipo):
            conn_db.insertar("tipos", {"nombre": tipo})

    # Procesar TIPO DE PAGO
    tipo_pago = form['tipo_pago']
    if tipo_pago == "__nuevo__":
        tipo_pago = form['nuevo_tipo_pago'].strip()
        if tipo_pago and not conn_db.existe_registro("tipos_pago", "nombre", tipo_pago):
            conn_db.insertar("tipos_pago", {"nombre": tipo_pago, "descripcion": "Agregado desde formulario"})

    # Procesar SERVICIOS
    servicios = form.getlist('servicios')
    print("Servicios seleccionados:", servicios)

    if "__nuevo__" in servicios:
        nuevo_servicio = form.get("nuevo_servicio", "").strip()
        print("Nuevo servicio ingresado:", nuevo_servicio)
        if nuevo_servicio:
            servicios.remove("__nuevo__")
            servicios.append(nuevo_servicio)

            if not conn_db.existe_registro("servicios", "nombre", nuevo_servicio):
                conn_db.insertar("servicios", {"nombre": nuevo_servicio})

    # Crear objeto Orden
    orden = Orden(
        nombre=form['nombre'],
        telefono=form['telefono'],
        correo=form['correo'],
        tipo=tipo,
        marca=form['marca'],
        modelo=form['modelo'],
        estado_entrada=form['estado_entrada'],
        servicios=servicios,
        perifericos=form['perifericos'],
        observaciones=form['observaciones'],
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tipo_pago=tipo_pago,
        pago=float(form.get('pago', 0)),
        estado=0  # Estado inicial: recibido
    )

    orden_dict = orden.a_dict()

    # Convertir servicios (lista) a texto para guardarlo en SQLite
    orden_dict['servicios'] = json.dumps(servicios)  # o ", ".join(servicios)

    # Guardar localmente
    conn_db.insertar("ordenes", orden_dict)

    print("✅ Orden registrada correctamente.")
    return redirect(url_for('index'))
@app.route('/api/tipos')
def api_tipos():
    tipos = conn_db.seleccionar("tipos", "nombre")
    return jsonify([{"nombre": t[0]} for t in tipos])


@app.route('/api/servicios')
def api_servicios():
    servicios = conn_db.seleccionar("servicios", "nombre")
    return jsonify([{"nombre": s[0]} for s in servicios])

@app.route('/api/tipos_pago')
def api_tipos_pago():
    tipos_pago = conn_db.seleccionar("tipos_pago", "nombre")
    return jsonify([{"nombre": t[0]} for t in tipos_pago])
89

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
