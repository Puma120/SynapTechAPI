from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

class GoogleCalendarService:
    """Servicio para integracion con Google Calendar"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.credentials = None
        self.service = None
    
    def get_auth_url(self, redirect_uri):
        """Obtener URL de autorizacion de Google"""
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [redirect_uri]
                    }
                },
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            return auth_url
            
        except Exception as e:
            print(f"Error al obtener URL de autorizacion: {str(e)}")
            return None
    
    def exchange_code_for_token(self, code, redirect_uri):
        """Intercambiar codigo de autorizacion por token"""
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [redirect_uri]
                    }
                },
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            flow.fetch_token(code=code)
            self.credentials = flow.credentials
            
            return {
                'token': self.credentials.token,
                'refresh_token': self.credentials.refresh_token,
                'token_uri': self.credentials.token_uri,
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'scopes': self.credentials.scopes
            }
            
        except Exception as e:
            print(f"Error al intercambiar codigo: {str(e)}")
            return None
    
    def initialize_service(self, credentials_dict):
        """Inicializar servicio con credenciales"""
        try:
            self.credentials = Credentials(
                token=credentials_dict['token'],
                refresh_token=credentials_dict.get('refresh_token'),
                token_uri=credentials_dict['token_uri'],
                client_id=credentials_dict['client_id'],
                client_secret=credentials_dict['client_secret'],
                scopes=credentials_dict['scopes']
            )
            
            self.service = build('calendar', 'v3', credentials=self.credentials)
            return True
            
        except Exception as e:
            print(f"Error al inicializar servicio: {str(e)}")
            return False
    
    def create_event(self, task):
        """Crear evento en Google Calendar desde tarea"""
        if not self.service:
            return None
        
        try:
            # Preparar evento
            event = {
                'summary': task.get('title'),
                'description': task.get('description', ''),
                'start': {
                    'dateTime': task.get('due_date'),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (datetime.fromisoformat(task.get('due_date').replace('Z', '+00:00')) + timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            # Crear evento
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            return created_event.get('id')
            
        except Exception as e:
            print(f"Error al crear evento: {str(e)}")
            return None
    
    def update_event(self, event_id, task):
        """Actualizar evento existente"""
        if not self.service:
            return False
        
        try:
            event = {
                'summary': task.get('title'),
                'description': task.get('description', ''),
            }
            
            if task.get('due_date'):
                event['start'] = {
                    'dateTime': task.get('due_date'),
                    'timeZone': 'UTC',
                }
                event['end'] = {
                    'dateTime': (datetime.fromisoformat(task.get('due_date').replace('Z', '+00:00')) + timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                }
            
            self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"Error al actualizar evento: {str(e)}")
            return False
    
    def delete_event(self, event_id):
        """Eliminar evento de calendario"""
        if not self.service:
            return False
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"Error al eliminar evento: {str(e)}")
            return False
    
    def list_events(self, max_results=10):
        """Listar proximos eventos"""
        if not self.service:
            return []
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            return events
            
        except Exception as e:
            print(f"Error al listar eventos: {str(e)}")
            return []
