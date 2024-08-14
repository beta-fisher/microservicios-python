from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import users_db
from utils import validate_password
import json

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Ruta para el registro de usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Validar entrada
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    # Validar si el usuario ya existe
    if username_or_email in users_db:
        return jsonify({"error": "El usuario ya existe."}), 400

    # Validar la longitud y complejidad de la contraseña
    if not validate_password(password):
        return jsonify({"error": "La contraseña no cumple con los criterios de seguridad."}), 400

    # Encriptar la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Registrar al usuario en la base de datos simulada
    users_db[username_or_email] = {
        "username": username_or_email,
        "password": hashed_password,
        "email": username_or_email
    }

    return jsonify({"message": "Usuario registrado exitosamente."}), 201

# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Validar entrada
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    # Validar la longitud y complejidad de la contraseña
    if not validate_password(password):
        return jsonify({"error": "La contraseña no cumple con los criterios de seguridad."}), 400

    # Verificar si el usuario existe (simulado aquí con un diccionario en memoria)
    user = users_db.get(username_or_email)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404
    
    # Verificar la contraseña encriptada
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Contraseña incorrecta."}), 401

    return jsonify({"message": "Login exitoso."}), 200

# Ruta de db
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users_db), 200

'''
##############################################################
                        MICROSERVICIO
##############################################################
'''

# Lista de videojuegos
videojuegos = [
    {
        "id": 1,
        "nombre": "The Legend of Zelda: Breath of the Wild",
        "precio_compra": 59.99,
        "precio_venta": 79.99,
        "plataforma": "Switch",
        "descripcion": "Un juego de acción y aventura en un mundo abierto.",
        "stock": 25,
        "valoracion": 9.8,
        "image": "https://example.com/images/zelda.jpg"
    },
    {
        "id": 2,
        "nombre": "Super Mario Odyssey",
        "precio_compra": 49.99,
        "precio_venta": 69.99,
        "plataforma": "Switch",
        "descripcion": "Una aventura de plataformas en 3D con Mario.",
        "stock": 30,
        "valoracion": 9.5,
        "image": "https://example.com/images/mario.jpg"
    },
    {
        "id": 3,
        "nombre": "Red Dead Redemption 2",
        "precio_compra": 69.99,
        "precio_venta": 89.99,
        "plataforma": "PC",        
        "descripcion": "Un juego de acción y aventura en el salvaje oeste.",
        "stock": 15,
        "valoracion": 9.7,
        "image": "https://example.com/images/red_dead.jpg"
    }
]

# Obtener todos los videojuegos
@app.route('/videojuegos', methods=['GET'])
def get_all_games():
    return jsonify(videojuegos)

# Obtener un videojuego por ID
@app.route('/videojuegos/<int:videojuego_id>', methods=['GET'])
def get_game_by_id(videojuego_id):
    videojuego = next((v for v in videojuegos if v["id"] == videojuego_id), None)
    if videojuego is None:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    return jsonify(videojuego)

# Agregar un nuevo videojuego
@app.route('/videojuegos', methods=['POST'])
def create_game():
    data = request.get_json()
    data['id'] = max((v['id'] for v in videojuegos), default=0) + 1
    videojuegos.append(data)
    return jsonify(data), 201

# Eliminar un videojuego
@app.route('/videojuegos/<int:videojuego_id>', methods=['DELETE'])
def delete_game(videojuego_id):
    global videojuegos
    videojuego = next((v for v in videojuegos if v['id'] == videojuego_id), None)
    if videojuego is None:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    
    videojuegos = [v for v in videojuegos if v['id'] != videojuego_id]
    return jsonify({"message": "Videojuego eliminado exitosamente"}), 200

# Modificar un videojuego
@app.route('/videojuegos/<int:videojuego_id>', methods=['PUT'])
def update_game(videojuego_id):
    data = request.get_json()
    
    # Validar datos de entrada
    required_keys = ['nombre', 'precio_compra', 'precio_venta', 'plataforma', 'descripcion', 'stock', 'valoracion', 'image']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Faltan datos en la solicitud"}), 400
    
    videojuego = next((v for v in videojuegos if v['id'] == videojuego_id), None)
    if videojuego is None:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    
    # Actualizar videojuego
    for key, value in data.items():
        if key in videojuego:
            videojuego[key] = value
    
    return jsonify(videojuego)

if __name__ == '__main__':
    app.run(debug=True)