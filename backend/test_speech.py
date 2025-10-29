"""Script de prueba para transcripción de audio"""
import os
import sys

# Agregar el path del backend al PYTHONPATH
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

from app.services.speech_service import SpeechService

def test_transcription():
    """Prueba la transcripción de un archivo de audio"""
    
    # Ruta al archivo de audio de prueba
    audio_file = os.path.join(backend_path, "app", "utils", "Audio_Sample2.wav")
    
    if not os.path.exists(audio_file):
        print(f"❌ Error: No se encontró el archivo de audio en: {audio_file}")
        print("Por favor, coloca un archivo WAV de prueba en app/utils/Audio_Sample.wav")
        return
    
    print(f"📁 Usando archivo: {audio_file}")
    print(f"📏 Tamaño: {os.path.getsize(audio_file)} bytes")
    print()
    
    try:
        # Crear instancia del servicio
        speech_service = SpeechService()
        
        print("🎤 Transcribiendo audio...")
        transcript = speech_service.transcribe_audio_file(audio_file, language_code="es-MX")
        
        print()
        print("✅ Transcripción exitosa!")
        print(f"📝 Texto: \"{transcript}\"")
        print()
        
    except Exception as e:
        print()
        print(f"❌ Error durante la transcripción: {str(e)}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE TRANSCRIPCIÓN DE AUDIO")
    print("=" * 60)
    print()
    test_transcription()
