import google.generativeai as genai
import os
from config import Config

class GeminiService:
    """Servicio para interactuar con Google Gemini AI"""
    
    def __init__(self):
        api_key = Config.GEMINI_API_KEY
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-2.5')
        else:
            self.model = None
    
    def transcribe_voice_to_task(self, voice_text):
        """
        Transcribe texto de voz y extrae informacion de tarea
        Retorna un diccionario con titulo, descripcion, prioridad, etc.
        """
        if not self.model:
            return {
                'title': voice_text[:100],
                'description': voice_text,
                'priority': 'medium',
                'category': None
            }
        
        try:
            prompt = f"""
            Analiza el siguiente texto de voz y extrae informacion para crear una tarea:
            
            "{voice_text}"
            
            Extrae y devuelve en formato JSON:
            - title: titulo corto de la tarea (maximo 100 caracteres)
            - description: descripcion detallada
            - priority: prioridad (low, medium, high, urgent)
            - category: categoria sugerida (personal, trabajo, salud, otros)
            - suggested_time: tiempo sugerido para completar (en minutos)
            
            Responde SOLO con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            
            # Parsear respuesta
            import json
            result = json.loads(response.text.strip())
            
            return result
            
        except Exception as e:
            print(f"Error en transcripcion: {str(e)}")
            return {
                'title': voice_text[:100],
                'description': voice_text,
                'priority': 'medium',
                'category': None
            }
    
    def prioritize_tasks(self, tasks, user_patterns=None):
        """
        Analiza tareas y sugiere priorizacion basada en:
        - Fechas de vencimiento
        - Patrones historicos del usuario
        - Urgencia y importancia
        """
        if not self.model or not tasks:
            return tasks
        
        try:
            tasks_summary = []
            for task in tasks:
                tasks_summary.append({
                    'id': task.get('id'),
                    'title': task.get('title'),
                    'priority': task.get('priority'),
                    'due_date': task.get('due_date'),
                    'category': task.get('category')
                })
            
            prompt = f"""
            Analiza las siguientes tareas y sugiere un orden de priorizacion para una persona con ADHD.
            Considera:
            - Urgencia (fechas de vencimiento)
            - Importancia
            - Carga cognitiva
            - Momento del dia optimo
            
            Tareas: {tasks_summary}
            
            Patrones del usuario: {user_patterns if user_patterns else "No disponible"}
            
            Devuelve un JSON con:
            - task_id: orden sugerido (1, 2, 3, etc)
            - reason: breve explicacion
            - suggested_time_of_day: manana, tarde, noche
            
            Responde SOLO con el JSON array, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            
            import json
            prioritization = json.loads(response.text.strip())
            
            return prioritization
            
        except Exception as e:
            print(f"Error en priorizacion: {str(e)}")
            return []
    
    def generate_routine_suggestions(self, user_tasks, time_of_day):
        """
        Genera sugerencias de rutinas basadas en tareas del usuario
        """
        if not self.model:
            return []
        
        try:
            prompt = f"""
            Basandote en las tareas de un usuario con ADHD, sugiere rutinas efectivas para {time_of_day}.
            
            Tareas comunes: {[t.get('title') for t in user_tasks[:10]]}
            
            Genera 3 sugerencias de rutinas que incluyan:
            - name: nombre de la rutina
            - description: descripcion breve
            - steps: lista de pasos con titulo y duracion estimada (minutos)
            - recommended_frequency: daily o weekly
            
            Las rutinas deben ser:
            - Simples y faciles de seguir
            - Con pasos claros y concretos
            - Adaptadas para personas con ADHD
            
            Responde SOLO con el JSON array, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            
            import json
            suggestions = json.loads(response.text.strip())
            
            return suggestions
            
        except Exception as e:
            print(f"Error en sugerencias: {str(e)}")
            return []
    
    def generate_reminder_message(self, task):
        """
        Genera un mensaje de recordatorio personalizado y discreto
        """
        if not self.model:
            return f"Recordatorio: {task.get('title')}"
        
        try:
            prompt = f"""
            Genera un mensaje de recordatorio discreto y motivador para la siguiente tarea:
            
            Titulo: {task.get('title')}
            Descripcion: {task.get('description', '')}
            Prioridad: {task.get('priority')}
            
            El mensaje debe ser:
            - Corto (maximo 50 caracteres)
            - Positivo y motivador
            - Sin emojis
            - Directo y claro
            
            Responde SOLO con el mensaje, sin comillas ni texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            message = response.text.strip().replace('"', '')
            
            return message[:50]
            
        except Exception as e:
            print(f"Error en mensaje: {str(e)}")
            return f"Recordatorio: {task.get('title')}"
    
    def analyze_productivity_patterns(self, metrics_data):
        """
        Analiza metricas de productividad y genera insights
        """
        if not self.model:
            return {
                'insights': 'Datos insuficientes para analisis',
                'recommendations': []
            }
        
        try:
            prompt = f"""
            Analiza los siguientes datos de productividad de un usuario con ADHD:
            
            {metrics_data}
            
            Genera:
            - insights: 3 observaciones principales sobre patrones de productividad
            - recommendations: 3 recomendaciones especificas para mejorar
            - best_time_slots: mejores momentos del dia para tareas importantes
            
            Responde SOLO con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            
            import json
            analysis = json.loads(response.text.strip())
            
            return analysis
            
        except Exception as e:
            print(f"Error en analisis: {str(e)}")
            return {
                'insights': ['Error al analizar datos'],
                'recommendations': [],
                'best_time_slots': []
            }
