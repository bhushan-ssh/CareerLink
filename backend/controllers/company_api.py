from flask_security import current_user
from controllers.models import Company, Job, Application, Student
from flask_restful import Resource
from controllers.database import db
from flask import request, make_response, jsonify
from flask_security import auth_token_required, roles_required
from datetime import datetime

from controllers.cache import cache

class CompanyJobsAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        if not company or not company.is_approved:
            return make_response(jsonify({'message': 'Company not found or not approved'}), 403)
            
        jobs = Job.query.filter_by(company_id=company.id).all()
        result = []
        for j in jobs:
            result.append({
                'id': j.id,
                'title': j.title,
                'description': j.description,
                'skills': j.skills,
                'experience': j.experience,
                'salary': j.salary,
                'benefits': j.benefits,
                'location': j.location,
                'deadline': j.deadline.isoformat() if j.deadline else None,
                'is_active': j.is_active,
                'created_at': j.created_at.isoformat() if j.created_at else None
            })
        
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('company')
    def post(self):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        if not company or not company.is_approved:
            return make_response(jsonify({'message': 'Company not found or not approved'}), 403)
            
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
            
        title = data.get('title')
        description = data.get('description')
        deadline_str = data.get('deadline')
        
        if not title or not description or not deadline_str:
            return make_response(jsonify({'message': 'Title, description and deadline are required'}), 400)
            
        try:
            deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        except ValueError:
            return make_response(jsonify({'message': 'Invalid deadline format'}), 400)
            
        job = Job(
            company_id=company.id,
            title=title,
            description=description,
            skills=data.get('skills'),
            experience=data.get('experience'),
            salary=data.get('salary'),
            benefits=data.get('benefits'),
            location=data.get('location'),
            deadline=deadline
        )
        db.session.add(job)
        db.session.commit()
        cache.clear()
        
        response = make_response(jsonify({'message': 'Job posted successfully!'}), 201)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class CompanyJobDetailAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def put(self, job_id):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        if not company or not company.is_approved:
            return make_response(jsonify({'message': 'Company not found or not approved'}), 403)
            
        job = Job.query.filter_by(id=job_id, company_id=company.id).first()
        if not job:
            return make_response(jsonify({'message': 'Job not found'}), 404)
            
        data = request.get_json()
        if 'is_active' in data:
            job.is_active = data['is_active']
            db.session.commit()
            cache.clear()
            
        response = make_response(jsonify({'message': 'Job updated successfully!'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class CompanyApplicationsAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self, job_id):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        if not company:
            return make_response(jsonify({'message': 'Company not found'}), 403)
            
        # Verify job belongs to this company
        job = Job.query.filter_by(id=job_id, company_id=company.id).first()
        if not job:
            return make_response(jsonify({'message': 'Job not found'}), 404)
            
        applications = Application.query.filter_by(job_id=job_id).all()
        result = []
        for app in applications:
            student = Student.query.get(app.student_id)
            result.append({
                'id': app.id,
                'student_name': student.full_name if student else 'Unknown',
                'student_email': student.user.email if student and student.user else '',
                'student_resume': student.resume_filename if student else '',
                'student_skills': student.skills if student else '',
                'student_cgpa': student.cgpa if student else None,
                'status': app.status,
                'feedback': app.feedback,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'applied_at': app.applied_at.isoformat() if app.applied_at else None
            })
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class CompanyApplicationActionAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def put(self, app_id):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        if not company:
            return make_response(jsonify({'message': 'Company not found'}), 403)
            
        application = Application.query.get(app_id)
        if not application:
            return make_response(jsonify({'message': 'Application not found'}), 404)
            
        job = Job.query.get(application.job_id)
        if not job or job.company_id != company.id:
            return make_response(jsonify({'message': 'Unauthorized to modify this application'}), 403)
            
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
            
        if 'status' in data:
            new_status = data['status']
            application.status = new_status
            
            # If status is Placed, create a record in the Placements table if not exists
            if new_status == 'Placed':
                from controllers.models import Placement
                existing_placement = Placement.query.filter_by(application_id=application.id).first()
                if not existing_placement:
                    placement = Placement(
                        student_id=application.student_id,
                        company_id=job.company_id,
                        job_id=job.id,
                        application_id=application.id,
                        salary=job.salary # default to job salary
                    )
                    db.session.add(placement)
        
        if 'feedback' in data:
            application.feedback = data['feedback']
        if 'interview_date' in data:
            # allow clearing or setting
            date_str = data['interview_date']
            if date_str:
                try:
                    application.interview_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    return make_response(jsonify({'message': 'Invalid interview date format'}), 400)
            else:
                application.interview_date = None
                
        db.session.commit()
        response = make_response(jsonify({'message': 'Application updated successfully!'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response
