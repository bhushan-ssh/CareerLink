from flask_restful import Resource
from flask_security import auth_token_required, current_user
from flask import jsonify, make_response, send_file
import os
from controllers.tasks import export_applications_csv
from celery.result import AsyncResult

class ExportCSVAPI(Resource):
    @auth_token_required
    def post(self):
        # Determine whether user is student or company
        if current_user.has_role('student') and current_user.student_profile:
            task = export_applications_csv.delay('student', current_user.student_profile.id)
        elif current_user.has_role('company') and current_user.company_profile:
            task = export_applications_csv.delay('company', current_user.company_profile.id)
        else:
            return make_response(jsonify({'error': 'Unauthorized role for export'}), 403)
            
        return make_response(jsonify({'task_id': task.id}), 202)

class ExportStatusAPI(Resource):
    @auth_token_required
    def get(self, task_id):
        from app import celery_app
        # We can poll this endpoint from frontend to get task status
        result = AsyncResult(task_id, app=celery_app)
        
        if result.state == 'PENDING':
            response = {'state': result.state, 'status': 'Pending...'}
        elif result.state != 'FAILURE':
            response = {
                'state': result.state,
                'result': result.info, # Contains our {"status": "Complete", "file_name": ...} return value
            }
        else:
            response = {
                'state': result.state,
                'status': str(result.info),
            }
            
        return make_response(jsonify(response), 200)

class ExportDownloadAPI(Resource):
    @auth_token_required
    def get(self, file_name):
        export_dir = os.path.join(os.getcwd(), 'exports')
        file_path = os.path.join(export_dir, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='export.csv')
        return make_response(jsonify({'error': 'File not found'}), 404)
