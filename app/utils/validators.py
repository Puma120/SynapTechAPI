import re

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Valida la fortaleza de la contrasena
    Minimo 8 caracteres, al menos una mayuscula, una minuscula y un numero
    """
    if len(password) < 8:
        return False, 'La contrasena debe tener al menos 8 caracteres'
    
    if not re.search(r'[A-Z]', password):
        return False, 'La contrasena debe contener al menos una mayuscula'
    
    if not re.search(r'[a-z]', password):
        return False, 'La contrasena debe contener al menos una minuscula'
    
    if not re.search(r'\d', password):
        return False, 'La contrasena debe contener al menos un numero'
    
    return True, None
