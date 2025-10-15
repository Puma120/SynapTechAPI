from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import pandas as pd

class ReportService:
    """Servicio para generacion de reportes"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generate_pdf_report(self, user, metrics, tasks, routines):
        """Generar reporte en PDF"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            story = []
            
            # Titulo
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2E3B4E')
            )
            
            story.append(Paragraph(f"Reporte de Productividad - {user.full_name}", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Fecha
            story.append(Paragraph(
                f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                self.styles['Normal']
            ))
            story.append(Spacer(1, 0.2*inch))
            
            # Resumen de metricas
            story.append(Paragraph("Resumen de Metricas", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            metrics_data = [
                ['Metrica', 'Valor'],
                ['Tareas completadas', str(metrics.get('tasks_completed', 0))],
                ['Tareas creadas', str(metrics.get('tasks_created', 0))],
                ['Rutinas seguidas', str(metrics.get('routines_followed', 0))],
                ['Recordatorios reconocidos', str(metrics.get('reminders_acknowledged', 0))],
                ['Tiempo total de enfoque', f"{metrics.get('total_focus_time', 0)} minutos"],
            ]
            
            metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Tareas recientes
            story.append(Paragraph("Tareas Recientes", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for task in tasks[:10]:
                status_icon = "[X]" if task['status'] == 'completed' else "[ ]"
                task_text = f"{status_icon} {task['title']} - Prioridad: {task['priority']}"
                story.append(Paragraph(task_text, self.styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Rutinas activas
            story.append(Paragraph("Rutinas Activas", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for routine in routines:
                if routine['is_active']:
                    routine_text = f"- {routine['name']} ({routine['frequency']})"
                    story.append(Paragraph(routine_text, self.styles['Normal']))
                    story.append(Spacer(1, 0.05*inch))
            
            # Generar PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return None
    
    def generate_csv_report(self, tasks, metrics):
        """Generar reporte en CSV"""
        try:
            # Crear DataFrame de tareas
            tasks_df = pd.DataFrame(tasks)
            
            # Crear DataFrame de metricas
            metrics_df = pd.DataFrame([metrics])
            
            # Generar CSV
            buffer = BytesIO()
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                tasks_df.to_excel(writer, sheet_name='Tareas', index=False)
                metrics_df.to_excel(writer, sheet_name='Metricas', index=False)
            
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            print(f"Error al generar CSV: {str(e)}")
            return None
    
    def calculate_productivity_score(self, metrics):
        """Calcular puntaje de productividad"""
        try:
            # Algoritmo simple de scoring
            tasks_completed = metrics.get('tasks_completed', 0)
            tasks_created = metrics.get('tasks_created', 0)
            routines_followed = metrics.get('routines_followed', 0)
            reminders_acknowledged = metrics.get('reminders_acknowledged', 0)
            
            # Tasa de completitud
            completion_rate = tasks_completed / tasks_created if tasks_created > 0 else 0
            
            # Puntaje base
            score = (completion_rate * 40) + (routines_followed * 2) + (reminders_acknowledged * 1)
            
            # Normalizar a 100
            score = min(score, 100)
            
            return {
                'score': round(score, 2),
                'completion_rate': round(completion_rate * 100, 2),
                'level': self._get_productivity_level(score)
            }
            
        except Exception as e:
            print(f"Error al calcular score: {str(e)}")
            return {'score': 0, 'completion_rate': 0, 'level': 'Bajo'}
    
    def _get_productivity_level(self, score):
        """Determinar nivel de productividad"""
        if score >= 80:
            return 'Excelente'
        elif score >= 60:
            return 'Bueno'
        elif score >= 40:
            return 'Moderado'
        else:
            return 'Bajo'
