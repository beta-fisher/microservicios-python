from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:123456@localhost/nombre_base_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Importar y registrar el Blueprint de videojuegos
from app.routes import videojuegos_bp
app.register_blueprint(videojuegos_bp)

# Importar rutas para que se registren con la aplicación
from app import models
