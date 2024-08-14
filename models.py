from flask_bcrypt import generate_password_hash

# Base de datos simulada de usuarios
users_db = {
    "user@example.com": {
        "username": "user1",
        "password": generate_password_hash("Password!1").decode('utf-8'),  # Contraseña encriptada
        "email": "user@example.com"
    },
    "user1": {
        "username": "user1",
        "password": generate_password_hash("Password!1").decode('utf-8'),  # Contraseña encriptada
        "email": "user@example.com"
    }
}