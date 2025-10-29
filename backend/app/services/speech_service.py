"""Servicio de transcripción de audio usando Google Cloud Speech-to-Text"""
import os
import base64
import wave
from google.cloud import speech_v1
from google.oauth2 import service_account
from config import Config

class SpeechService:
    """Servicio para transcribir audio a texto usando Google Cloud Speech-to-Text"""
    
    def __init__(self):
        # Configurar credenciales desde la API key
        self.api_key = Config.SPEECH_API_KEY
        
        # Cliente de Speech-to-Text
        if self.api_key:
            # Para usar con API Key directamente, usaremos la REST API
            self.client = None
            self.use_rest_api = True
        else:
            self.client = None
            self.use_rest_api = False
    
    def get_wav_info(self, audio_content):
        """
        Extrae información del archivo WAV
        
        Returns:
            dict: {'sample_rate': int, 'channels': int}
        """
        import io
        
        try:
            # Crear un buffer de bytes
            audio_buffer = io.BytesIO(audio_content)
            
            # Abrir como archivo WAV
            with wave.open(audio_buffer, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                
                return {
                    'sample_rate': sample_rate,
                    'channels': channels
                }
        except Exception as e:
            # Si no es un WAV válido, usar valores por defecto
            return {
                'sample_rate': 16000,
                'channels': 1
            }
    
    def transcribe_audio(self, audio_content, language_code="es-MX"):
        """
        Transcribe audio a texto
        
        Args:
            audio_content: bytes del archivo de audio (WAV recomendado)
            language_code: Código de idioma (default: es-MX para español de México)
        
        Returns:
            str: Texto transcrito del audio
        """
        if not self.api_key:
            raise Exception("SPEECH_API_KEY no configurada")
        
        try:
            # Usar la REST API con la API key
            import requests
            
            # Obtener información del audio
            wav_info = self.get_wav_info(audio_content)
            sample_rate = wav_info['sample_rate']
            
            # Codificar audio en base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            
            # Configuración de reconocimiento
            config = {
                "encoding": "LINEAR16",  # WAV format
                "sampleRateHertz": sample_rate,  # Usar la tasa de muestreo detectada
                "languageCode": language_code,
                "enableAutomaticPunctuation": True
            }
            
            # Request body
            request_body = {
                "config": config,
                "audio": {
                    "content": audio_base64
                }
            }
            
            # Llamar a la API
            url = f"https://speech.googleapis.com/v1/speech:recognize?key={self.api_key}"
            response = requests.post(url, json=request_body)
            
            if response.status_code != 200:
                raise Exception(f"Error en Speech API: {response.text}")
            
            result = response.json()
            
            # Extraer el texto transcrito
            if 'results' in result and len(result['results']) > 0:
                transcript = result['results'][0]['alternatives'][0]['transcript']
                return transcript
            else:
                return ""
        
        except Exception as e:
            print(f"Error transcribiendo audio: {str(e)}")
            raise Exception(f"Error al transcribir audio: {str(e)}")
    
    def transcribe_audio_file(self, file_path, language_code="es-MX"):
        """
        Transcribe un archivo de audio a texto
        
        Args:
            file_path: Ruta al archivo de audio
            language_code: Código de idioma
        
        Returns:
            str: Texto transcrito
        """
        try:
            with open(file_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            return self.transcribe_audio(audio_content, language_code)
        
        except Exception as e:
            raise Exception(f"Error al leer archivo de audio: {str(e)}")

# Instancia singleton
speech_service = SpeechService()
