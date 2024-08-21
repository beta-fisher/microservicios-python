from flask import Blueprint, request, jsonify
from app import app, db, bcrypt
from app.models import Videojuego
from app.models import User
from app.utils import validate_password

# Define el Blueprint
auth_bp = Blueprint('auth', __name__)

# Definir el register
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    if User.query.filter_by(username=username_or_email).first() or User.query.filter_by(email=username_or_email).first():
        return jsonify({"error": "El usuario ya existe."}), 400

    if not validate_password(password):
        return jsonify({"error": "La contraseña no cumple con los criterios de seguridad."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username_or_email, email=username_or_email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente."}), 201

# Definir el login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Contraseña incorrecta."}), 401

    return jsonify({"message": "Login exitoso."}), 200

# Define el Blueprint
videojuegos_bp = Blueprint('videojuegos', __name__)

# Obtener todos los videojuegos
@videojuegos_bp.route('/videojuegos', methods=['GET'])
def get_all_games():
    juegos = Videojuego.query.all()
    return jsonify([{
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    } for juego in juegos])

# Obtener un videojuego por ID
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['GET'])
def get_game_by_id(videojuego_id):
    juego = Videojuego.query.get(videojuego_id)
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    return jsonify({
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    })

# Agregar un nuevo videojuego
@videojuegos_bp.route('/videojuegos', methods=['POST'])
def create_game():
    data = request.get_json()

    nuevo_juego = Videojuego(
        nombre=data['nombre'],
        precio_compra=data['precio_compra'],
        precio_venta=data['precio_venta'],
        plataforma=data['plataforma'],
        descripcion=data['descripcion'],
        stock=data['stock'],
        valoracion=data['valoracion'],
        image=data['image']
    )

    db.session.add(nuevo_juego)
    db.session.commit()

    return jsonify({
        "id": nuevo_juego.id,
        "nombre": nuevo_juego.nombre,
        "precio_compra": nuevo_juego.precio_compra,
        "precio_venta": nuevo_juego.precio_venta,
        "plataforma": nuevo_juego.plataforma,
        "descripcion": nuevo_juego.descripcion,
        "stock": nuevo_juego.stock,
        "valoracion": nuevo_juego.valoracion,
        "image": nuevo_juego.image
    }), 201

# Eliminar un videojuego
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['DELETE'])
def delete_game(videojuego_id):
    juego = Videojuego.query.get(videojuego_id)
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    
    db.session.delete(juego)
    db.session.commit()

    return jsonify({"message": "Videojuego eliminado exitosamente"}), 200

# Modificar un videojuego
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['PUT'])
def update_game(videojuego_id):
    data = request.get_json()
    juego = Videojuego.query.get(videojuego_id)
    
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404

    juego.nombre = data.get('nombre', juego.nombre)
    juego.precio_compra = data.get('precio_compra', juego.precio_compra)
    juego.precio_venta = data.get('precio_venta', juego.precio_venta)
    juego.plataforma = data.get('plataforma', juego.plataforma)
    juego.descripcion = data.get('descripcion', juego.descripcion)
    juego.stock = data.get('stock', juego.stock)
    juego.valoracion = data.get('valoracion', juego.valoracion)
    juego.image = data.get('image', juego.image)
    
    db.session.commit()

    return jsonify({
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    }), 200



'''
from flask import Blueprint, request, jsonify
from app import app, db, bcrypt
from app.models import User, Videojuego
from app.utils import validate_password


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    if User.query.filter_by(username=username_or_email).first() or User.query.filter_by(email=username_or_email).first():
        return jsonify({"error": "El usuario ya existe."}), 400

    if not validate_password(password):
        return jsonify({"error": "La contraseña no cumple con los criterios de seguridad."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username_or_email, email=username_or_email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({"error": "Debe proporcionar correo/nombre de usuario y contraseña."}), 400
    
    username_or_email = data['username_or_email']
    password = data['password']

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Contraseña incorrecta."}), 401

    return jsonify({"message": "Login exitoso."}), 200

# Rutas restantes (get_users, get_all_games, get_game_by_id, create_game, delete_game, update_game)

@videojuegos_bp.route('/videojuegos', methods=['GET'])
def get_all_games():
    juegos = Videojuego.query.all()
    return jsonify([{
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    } for juego in juegos])

# Obtener un videojuego por ID
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['GET'])
def get_game_by_id(videojuego_id):
    juego = Videojuego.query.get(videojuego_id)
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    return jsonify({
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    })

# Agregar un nuevo videojuego
@videojuegos_bp.route('/videojuegos', methods=['POST'])
def create_game():
    data = request.get_json()

    nuevo_juego = Videojuego(
        nombre=data['nombre'],
        precio_compra=data['precio_compra'],
        precio_venta=data['precio_venta'],
        plataforma=data['plataforma'],
        descripcion=data['descripcion'],
        stock=data['stock'],
        valoracion=data['valoracion'],
        image=data['image']
    )

    db.session.add(nuevo_juego)
    db.session.commit()

    return jsonify({
        "id": nuevo_juego.id,
        "nombre": nuevo_juego.nombre,
        "precio_compra": nuevo_juego.precio_compra,
        "precio_venta": nuevo_juego.precio_venta,
        "plataforma": nuevo_juego.plataforma,
        "descripcion": nuevo_juego.descripcion,
        "stock": nuevo_juego.stock,
        "valoracion": nuevo_juego.valoracion,
        "image": nuevo_juego.image
    }), 201

# Eliminar un videojuego
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['DELETE'])
def delete_game(videojuego_id):
    juego = Videojuego.query.get(videojuego_id)
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404
    
    db.session.delete(juego)
    db.session.commit()

    return jsonify({"message": "Videojuego eliminado exitosamente"}), 200

# Modificar un videojuego
@videojuegos_bp.route('/videojuegos/<int:videojuego_id>', methods=['PUT'])
def update_game(videojuego_id):
    data = request.get_json()
    juego = Videojuego.query.get(videojuego_id)
    
    if not juego:
        return jsonify({"error": "Videojuego no encontrado"}), 404

    juego.nombre = data.get('nombre', juego.nombre)
    juego.precio_compra = data.get('precio_compra', juego.precio_compra)
    juego.precio_venta = data.get('precio_venta', juego.precio_venta)
    juego.plataforma = data.get('plataforma', juego.plataforma)
    juego.descripcion = data.get('descripcion', juego.descripcion)
    juego.stock = data.get('stock', juego.stock)
    juego.valoracion = data.get('valoracion', juego.valoracion)
    juego.image = data.get('image', juego.image)
    
    db.session.commit()

    return jsonify({
        "id": juego.id,
        "nombre": juego.nombre,
        "precio_compra": juego.precio_compra,
        "precio_venta": juego.precio_venta,
        "plataforma": juego.plataforma,
        "descripcion": juego.descripcion,
        "stock": juego.stock,
        "valoracion": juego.valoracion,
        "image": juego.image
    }), 200
'''
