from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, date
from app import db
from app.models.user import User
from app.models.task import Task, Routine
from app.models.sync import ProductivityMetric, ReminderLog
from app.services.report_service import ReportService
from app.services.gemini_service import GeminiService

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')
report_service = ReportService()
gemini_service = GeminiService()

@reports_bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Obtener metricas de productividad"""
    try:
        user_id = get_jwt_identity()
        
        # Parametros de fecha
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).date()
        else:
            start_date = datetime.fromisoformat(start_date).date()
        
        if not end_date:
            end_date = datetime.now().date()
        else:
            end_date = datetime.fromisoformat(end_date).date()
        
        # Obtener metricas del periodo
        metrics = ProductivityMetric.query.filter(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= start_date,
            ProductivityMetric.date <= end_date
        ).all()
        
        # Calcular totales
        total_metrics = {
            'tasks_completed': sum(m.tasks_completed for m in metrics),
            'tasks_created': sum(m.tasks_created for m in metrics),
            'routines_followed': sum(m.routines_followed for m in metrics),
            'reminders_acknowledged': sum(m.reminders_acknowledged for m in metrics),
            'total_focus_time': sum(m.total_focus_time for m in metrics),
            'period_days': len(metrics)
        }
        
        # Calcular score de productividad
        productivity_score = report_service.calculate_productivity_score(total_metrics)
        
        return jsonify({
            'metrics': total_metrics,
            'productivity_score': productivity_score,
            'daily_metrics': [m.to_dict() for m in metrics]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener metricas: {str(e)}'}), 500

@reports_bp.route('/update-metrics', methods=['POST'])
@jwt_required()
def update_daily_metrics():
    """Actualizar metricas diarias"""
    try:
        user_id = get_jwt_identity()
        today = date.today()
        
        # Buscar o crear metrica del dia
        metric = ProductivityMetric.query.filter_by(
            user_id=user_id,
            date=today
        ).first()
        
        if not metric:
            metric = ProductivityMetric(
                user_id=user_id,
                date=today
            )
            db.session.add(metric)
        
        # Calcular metricas del dia
        tasks_completed = Task.query.filter(
            Task.user_id == user_id,
            Task.status == 'completed',
            Task.completed_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        tasks_created = Task.query.filter(
            Task.user_id == user_id,
            Task.created_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        reminders_acknowledged = ReminderLog.query.filter(
            ReminderLog.user_id == user_id,
            ReminderLog.was_acknowledged == True,
            ReminderLog.acknowledged_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        # Actualizar
        metric.tasks_completed = tasks_completed
        metric.tasks_created = tasks_created
        metric.reminders_acknowledged = reminders_acknowledged
        
        db.session.commit()
        
        return jsonify({
            'message': 'Metricas actualizadas',
            'metrics': metric.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar metricas: {str(e)}'}), 500

@reports_bp.route('/pdf', methods=['POST'])
@jwt_required()
def generate_pdf_report():
    """Generar reporte en PDF"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Obtener datos del usuario
        user = User.query.get(user_id)
        
        # Obtener metricas
        start_date = data.get('start_date')
        if start_date:
            start_date = datetime.fromisoformat(start_date).date()
        else:
            start_date = (datetime.now() - timedelta(days=30)).date()
        
        metrics_list = ProductivityMetric.query.filter(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= start_date
        ).all()
        
        total_metrics = {
            'tasks_completed': sum(m.tasks_completed for m in metrics_list),
            'tasks_created': sum(m.tasks_created for m in metrics_list),
            'routines_followed': sum(m.routines_followed for m in metrics_list),
            'reminders_acknowledged': sum(m.reminders_acknowledged for m in metrics_list),
            'total_focus_time': sum(m.total_focus_time for m in metrics_list)
        }
        
        # Obtener tareas recientes
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).limit(20).all()
        tasks_data = [t.to_dict() for t in tasks]
        
        # Obtener rutinas
        routines = Routine.query.filter_by(user_id=user_id).all()
        routines_data = [r.to_dict() for r in routines]
        
        # Generar PDF
        pdf_buffer = report_service.generate_pdf_report(
            user,
            total_metrics,
            tasks_data,
            routines_data
        )
        
        if not pdf_buffer:
            return jsonify({'error': 'Error al generar reporte'}), 500
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'reporte_synaptech_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error al generar PDF: {str(e)}'}), 500

@reports_bp.route('/csv', methods=['POST'])
@jwt_required()
def generate_csv_report():
    """Generar reporte en CSV"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Obtener tareas
        tasks = Task.query.filter_by(user_id=user_id).all()
        tasks_data = [t.to_dict() for t in tasks]
        
        # Obtener metricas
        start_date = data.get('start_date')
        if start_date:
            start_date = datetime.fromisoformat(start_date).date()
        else:
            start_date = (datetime.now() - timedelta(days=30)).date()
        
        metrics_list = ProductivityMetric.query.filter(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= start_date
        ).all()
        
        metrics_data = {
            'tasks_completed': sum(m.tasks_completed for m in metrics_list),
            'tasks_created': sum(m.tasks_created for m in metrics_list),
            'routines_followed': sum(m.routines_followed for m in metrics_list),
            'reminders_acknowledged': sum(m.reminders_acknowledged for m in metrics_list)
        }
        
        # Generar CSV
        csv_buffer = report_service.generate_csv_report(tasks_data, metrics_data)
        
        if not csv_buffer:
            return jsonify({'error': 'Error al generar reporte'}), 500
        
        return send_file(
            csv_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'reporte_synaptech_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error al generar CSV: {str(e)}'}), 500

@reports_bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    """Obtener insights de productividad con IA"""
    try:
        user_id = get_jwt_identity()
        
        # Obtener metricas del ultimo mes
        start_date = (datetime.now() - timedelta(days=30)).date()
        
        metrics = ProductivityMetric.query.filter(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= start_date
        ).all()
        
        metrics_data = [m.to_dict() for m in metrics]
        
        # Analizar con IA
        insights = gemini_service.analyze_productivity_patterns(metrics_data)
        
        return jsonify({
            'insights': insights
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener insights: {str(e)}'}), 500

@reports_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    """Obtener datos para dashboard"""
    try:
        user_id = get_jwt_identity()
        today = date.today()
        
        # Tareas de hoy
        today_tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.due_date >= datetime.combine(today, datetime.min.time()),
            Task.due_date < datetime.combine(today + timedelta(days=1), datetime.min.time()),
            Task.status != 'completed'
        ).all()
        
        # Tareas pendientes
        pending_tasks = Task.query.filter_by(
            user_id=user_id,
            status='pending'
        ).count()
        
        # Tareas completadas hoy
        completed_today = Task.query.filter(
            Task.user_id == user_id,
            Task.status == 'completed',
            Task.completed_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        # Rutinas activas
        active_routines = Routine.query.filter_by(
            user_id=user_id,
            is_active=True
        ).count()
        
        # Metricas de la semana
        week_start = today - timedelta(days=today.weekday())
        week_metrics = ProductivityMetric.query.filter(
            ProductivityMetric.user_id == user_id,
            ProductivityMetric.date >= week_start
        ).all()
        
        week_completion = sum(m.tasks_completed for m in week_metrics)
        
        return jsonify({
            'today_tasks': [t.to_dict() for t in today_tasks],
            'pending_tasks': pending_tasks,
            'completed_today': completed_today,
            'active_routines': active_routines,
            'week_completion': week_completion
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener dashboard: {str(e)}'}), 500
