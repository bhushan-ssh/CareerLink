from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore
from controllers.celery_app import celery_init_app
from controllers.cache import cache


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Security
    security = Security(app, user_datastore)
    api = Api(app, prefix='/api')
    # Initialize cache
    cache.init_app(app)



    with app.app_context():
        db.create_all()

        # Create roles if they don't exist
        admin_role= user_datastore.find_or_create_role(name='admin', description='Administrator')
        student_role= user_datastore.find_or_create_role(name='student', description='Student')
        company_role= user_datastore.find_or_create_role(name='company', description='Company')

        if not user_datastore.find_user(email='admin@gmail.com'):
            user_datastore.create_user(email='admin@gmail.com', password='admin', roles=[admin_role])

        db.session.commit()


    return app, api

app,api = create_app()
celery_app = celery_init_app(app)

import controllers.tasks
from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'send-interview-reminders': {
        'task': 'controllers.tasks.send_interview_reminders',
        'schedule': crontab(hour=0, minute=0),
    },
    'generate-monthly-reports': {
        'task': 'controllers.tasks.generate_monthly_placement_reports',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

CORS(app, expose_headers=['Authentication-Token'])



from controllers.auth_api import LoginAPI, LogoutAPI, RegisterAPI, check_email_availabilityAPI, Student_DashAPI, StudentProfileAPI, Company_DashAPI, CompanyProfileAPI
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')
api.add_resource(check_email_availabilityAPI, '/check_email')
api.add_resource(Student_DashAPI, '/student_dash')
api.add_resource(StudentProfileAPI, '/student_profile')
api.add_resource(Company_DashAPI, '/company_dash')
api.add_resource(CompanyProfileAPI, '/company_profile')

# New Admin APIs
from controllers.admin_api import AdminDashboardStatsAPI, AdminCompanyManagementAPI, \
                                 AdminStudentManagementAPI, AdminJobManagementAPI, AdminApplicationManagementAPI, AdminPlacementManagementAPI
api.add_resource(AdminDashboardStatsAPI, '/admin/stats')
api.add_resource(AdminCompanyManagementAPI, '/admin/companies')
api.add_resource(AdminStudentManagementAPI, '/admin/students')
api.add_resource(AdminJobManagementAPI, '/admin/jobs')
api.add_resource(AdminApplicationManagementAPI, '/admin/applications')
api.add_resource(AdminPlacementManagementAPI, '/admin/placements')

from controllers.company_api import CompanyJobsAPI, CompanyJobDetailAPI, CompanyApplicationsAPI, CompanyApplicationActionAPI
api.add_resource(CompanyJobsAPI, '/company/jobs')
api.add_resource(CompanyJobDetailAPI, '/company/jobs/<int:job_id>')
api.add_resource(CompanyApplicationsAPI, '/company/jobs/<int:job_id>/applications')
api.add_resource(CompanyApplicationActionAPI, '/company/applications/<int:app_id>')

from controllers.student_api import StudentJobsAPI, StudentApplicationsAPI, StudentJobApplyAPI
api.add_resource(StudentJobsAPI, '/student/jobs')
api.add_resource(StudentApplicationsAPI, '/student/applications')
api.add_resource(StudentJobApplyAPI, '/student/jobs/<int:job_id>/apply')

from controllers.export_api import ExportCSVAPI, ExportStatusAPI, ExportDownloadAPI
api.add_resource(ExportCSVAPI, '/export')
api.add_resource(ExportStatusAPI, '/export/status/<string:task_id>')
api.add_resource(ExportDownloadAPI, '/export/download/<string:file_name>')

if __name__ == '__main__':
    app.run(debug=True)
