from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio_compra = db.Column(db.Float, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    valoracion = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(250), nullable=False)
