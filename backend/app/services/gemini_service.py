import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta
from config import Config

class GeminiService:
    """Servicio simplificado para IA con Gemini - Procesa tareas y genera rutinas"""
    
    def __init__(self):
        api_key = Config.GEMINI_API_KEY
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-3-pro-preview')
        else:
            self.model = None
    
    def process_task_input(self, body_text="", audio_file=None, fecha=None):
        """
        Procesa input del usuario (texto y/o audio) y extrae información de la tarea
        
        Args:
            body_text: Texto del cuerpo de la tarea (puede estar vacío)
            audio_file: Archivo de audio (opcional)
            fecha: Fecha sugerida por el usuario (opcional)
        
        Returns:
            dict: {
                'title': str,
                'priority': str (low, medium, high, urgent),
                'due_date': str (ISO format),
                'body': str (descripción refinada)
            }
        """
        if not self.model:
            # Fallback sin IA
            return {
                'title': body_text[:100] if body_text else "Nueva tarea",
                'priority': 'medium',
                'due_date': fecha if fecha else (datetime.now() + timedelta(days=1)).isoformat(),
                'body': body_text
            }
        
        try:
            # Si hay audio, transcribirlo primero
            transcribed_text = body_text
            if audio_file:
                # Aquí puedes usar la API de transcripción de Gemini si está disponible
                # Por ahora, asumimos que el audio viene como texto
                transcribed_text = audio_file
            
            # Prompt para el agente
            prompt = f"""
Eres un asistente personal especializado en ayudar a personas con ADHD a gestionar tareas.
Analiza el siguiente input del usuario y extrae la información clave para crear una tarea bien estructurada.

Input del usuario: "{transcribed_text}"
Fecha sugerida: {fecha if fecha else "No especificada"}

Tu tarea:
1. Extrae o genera un título claro y conciso (máximo 100 caracteres)
2. Determina la prioridad basándote en palabras clave:
   - urgent: si menciona "urgente", "ya", "ahora", "inmediato"
   - high: si menciona "importante", "pronto", "mañana"
   - medium: si menciona "cuando pueda", "esta semana"
   - low: si menciona "algún día", "no urgente", "eventualmente"
3. Establece una fecha de vencimiento realista:
   - Si el usuario dio una fecha, úsala
   - Si no, infiere basándote en la urgencia:
     * urgent: hoy
     * high: mañana
     * medium: dentro de 3 días
     * low: dentro de una semana
4. Refina el cuerpo/descripción: mejora la redacción y añade detalles útiles

Responde ÚNICAMENTE con un JSON válido en este formato exacto:
{{
    "title": "título aquí",
    "priority": "low|medium|high|urgent",
    "due_date": "YYYY-MM-DDTHH:MM:SS",
    "body": "descripción refinada aquí"
}}

NO añadas texto adicional, SOLO el JSON.
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Limpiar el texto si viene con markdown
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result = json.loads(result_text.strip())
            
            # Validar campos obligatorios
            if 'title' not in result:
                result['title'] = transcribed_text[:100]
            if 'priority' not in result or result['priority'] not in ['low', 'medium', 'high', 'urgent']:
                result['priority'] = 'medium'
            if 'due_date' not in result:
                result['due_date'] = (datetime.now() + timedelta(days=1)).isoformat()
            if 'body' not in result:
                result['body'] = transcribed_text
            
            return result
            
        except Exception as e:
            print(f"Error procesando tarea con IA: {str(e)}")
            # Fallback seguro
            return {
                'title': transcribed_text[:100] if transcribed_text else "Nueva tarea",
                'priority': 'medium',
                'due_date': fecha if fecha else (datetime.now() + timedelta(days=1)).isoformat(),
                'body': transcribed_text
            }
    
    def generate_routine_suggestions(self, user_tasks):
        """
        Genera rutinas dinámicas basadas en las tareas existentes del usuario
        
        Args:
            user_tasks: Lista de tareas del usuario con sus detalles
        
        Returns:
            list: [
                {
                    'id_tarea': int,
                    'cuerpo': str (sugerencia de cuándo/cómo hacerla)
                },
                ...
            ]
        """
        if not self.model or not user_tasks:
            # Fallback: devolver tareas sin procesamiento
            return [
                {
                    'id_tarea': task['id'],
                    'cuerpo': task.get('body', task['title'])
                }
                for task in user_tasks[:5]  # Máximo 5 tareas
            ]
        
        try:
            # Preparar resumen de tareas
            tasks_summary = []
            for task in user_tasks:
                tasks_summary.append({
                    'id': task['id'],
                    'title': task['title'],
                    'body': task.get('body', ''),
                    'priority': task.get('priority', 'medium'),
                    'due_date': task.get('due_date'),
                    'status': task.get('status', 'pending')
                })
            
            prompt = f"""
Eres un asistente personal especializado en ayudar a personas con ADHD a organizar su día.
Tienes acceso a las siguientes tareas pendientes del usuario:

{json.dumps(tasks_summary, indent=2, ensure_ascii=False)}

Tu objetivo:
1. Selecciona las 3-5 tareas más importantes para hoy/mañana
2. Para cada tarea, crea una sugerencia de rutina que incluya:
   - Momento óptimo del día para hacerla
   - Estimación de tiempo necesario
   - Consejos para completarla (especialmente útiles para ADHD)
   - Pasos concretos si la tarea es compleja

Considera:
- Tareas urgentes primero
- Agrupar tareas similares
- Alternar tareas difíciles con más sencillas
- Incluir breaks

Responde ÚNICAMENTE con un JSON válido en este formato exacto:
[
    {{
        "id_tarea": 123,
        "cuerpo": "Mañana (8:00-9:00) - 30min estimados\\n Pasos: ...\\n Consejo: ..."
    }},
    ...
]

NO añadas texto adicional, SOLO el JSON array.
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Limpiar el texto si viene con markdown
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result = json.loads(result_text.strip())
            
            return result
            
        except Exception as e:
            print(f"Error generando rutinas con IA: {str(e)}")
            # Fallback: devolver tareas prioritarias sin procesamiento
            sorted_tasks = sorted(
                user_tasks,
                key=lambda x: (
                    0 if x.get('priority') == 'urgent' else
                    1 if x.get('priority') == 'high' else
                    2 if x.get('priority') == 'medium' else 3
                )
            )
            return [
                {
                    'id_tarea': task['id'],
                    'cuerpo': f"{task['title']} - Prioridad: {task.get('priority', 'medium')}"
                }
                for task in sorted_tasks[:5]
            ]

# Instancia singleton
gemini_service = GeminiService()
