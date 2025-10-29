"""Script para probar el endpoint de crear tarea con audio"""
import os
import requests

# Configuración
#BASE_URL = "http://localhost:5000"  # Cambiar a URL de Render si es producción
BASE_URL = "https://synaptech-api.onrender.com"

def register_and_login():
    """Registra un usuario de prueba y obtiene el token"""
    print("🔐 Registrando usuario de prueba...")
    
    # Intentar login primero
    login_data = {
        "email": "test_audio@synaptech.com",
        "password": "Password123!"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        print("✅ Login exitoso")
        return response.json()['access_token']
    
    # Si no existe, registrar
    register_data = {
        "email": "test_audio@synaptech.com",
        "password": "Password123!",
        "name": "Usuario Prueba Audio"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    
    if response.status_code == 201:
        print("✅ Usuario registrado")
        return response.json()['access_token']
    else:
        print(f"❌ Error en registro: {response.text}")
        return None

def test_create_task_with_text(token):
    """Prueba crear tarea con texto simple"""
    print("\n" + "="*60)
    print("PRUEBA 1: Crear tarea con TEXTO")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "cuerpo": "Tengo que revisar los documentos urgentes mañana por la mañana"
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=data, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def test_create_task_with_audio(token):
    """Prueba crear tarea con archivo de audio"""
    print("\n" + "="*60)
    print("PRUEBA 2: Crear tarea con AUDIO")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Ruta al archivo de audio
    audio_file_path = os.path.join(
        os.path.dirname(__file__), 
        "app", 
        "utils", 
        "Audio_Sample.wav"
    )
    
    if not os.path.exists(audio_file_path):
        print(f"❌ No se encontró el archivo: {audio_file_path}")
        return False
    
    print(f"📁 Usando audio: {audio_file_path}")
    
    # Enviar solo el audio (sin texto)
    with open(audio_file_path, 'rb') as audio_file:
        files = {
            'audio': ('audio.wav', audio_file, 'audio/wav')
        }
        
        response = requests.post(
            f"{BASE_URL}/api/tasks", 
            files=files, 
            headers=headers
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def test_create_task_with_audio_and_text(token):
    """Prueba crear tarea con audio Y texto combinados"""
    print("\n" + "="*60)
    print("PRUEBA 3: Crear tarea con AUDIO + TEXTO")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    audio_file_path = os.path.join(
        os.path.dirname(__file__), 
        "app", 
        "utils", 
        "Audio_Sample.wav"
    )
    
    if not os.path.exists(audio_file_path):
        print(f"❌ No se encontró el archivo: {audio_file_path}")
        return False
    
    # Enviar audio + texto + fecha
    with open(audio_file_path, 'rb') as audio_file:
        files = {
            'audio': ('audio.wav', audio_file, 'audio/wav')
        }
        data = {
            'cuerpo': 'Nota adicional:',
            'fecha': '2025-10-30'
        }
        
        response = requests.post(
            f"{BASE_URL}/api/tasks", 
            files=files,
            data=data,
            headers=headers
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 201

def main():
    print("="*60)
    print("PRUEBAS DE ENDPOINT DE TAREAS CON AUDIO")
    print("="*60)
    print()
    
    # Obtener token
    token = register_and_login()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return
    
    print(f"Token: {token[:20]}...")
    
    # Ejecutar pruebas
    test1 = test_create_task_with_text(token)
    test2 = test_create_task_with_audio(token)
    test3 = test_create_task_with_audio_and_text(token)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"✅ Prueba 1 (Texto):        {'PASÓ' if test1 else 'FALLÓ'}")
    print(f"✅ Prueba 2 (Audio):        {'PASÓ' if test2 else 'FALLÓ'}")
    print(f"✅ Prueba 3 (Audio+Texto):  {'PASÓ' if test3 else 'FALLÓ'}")
    print()

if __name__ == "__main__":
    main()
