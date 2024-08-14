import re

def validate_password(password):
    """
    Valida si la contraseña cumple con los requisitos:
    - Longitud entre 8 y 15 caracteres.
    - Al menos una letra mayúscula.
    - Al menos una letra minúscula.
    - Al menos un carácter especial.
    """
    if len(password) < 8 or len(password) > 15:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'[¡"#$%&/()]', password):
        return False

    return True
