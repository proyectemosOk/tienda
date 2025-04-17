from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from firebase_config import ServicioFirebase
from orden import Orden 

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
firebase = ServicioFirebase("../proyectemosok-31150-firebase-adminsdk-fbsvc-fdae62578b.json")

@app.route('/')
def index():
    return render_template('orden.html')

@app.route('/orden')
def orden():
    return render_template('orden.html')

@app.route('/submit', methods=['POST'])
def submit():
    form = request.form
    orden = Orden(
        nombre=form['nombre'],
        telefono=form['telefono'],
        correo=form['correo'],
        tipo=form['tipo'],
        marca=form['marca'],
        modelo=form['modelo'],
        estado_entrada=form['estado_entrada'],
        servicios=form.getlist('servicios'),
        perifericos=form['perifericos'],
        observaciones=form['observaciones']
    )
    orden_id = firebase.crear_orden(orden.a_dict())
    print(f"Orden creada con ID: {orden_id}")
    return redirect(url_for('index'))

@app.route('/api/tipos')
def api_tipos():
    tipos = firebase.db.collection("tipos").stream()
    return jsonify([doc.to_dict() for doc in tipos])

@app.route('/api/servicios')
def api_servicios():
    servicios = firebase.db.collection("servicios").stream()
    print(servicios)
    return jsonify([doc.to_dict() for doc in servicios])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

