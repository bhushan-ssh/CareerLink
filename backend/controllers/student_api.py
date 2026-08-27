from flask_security import current_user
from controllers.models import Company, Job, Application, Student
from flask_restful import Resource
from controllers.database import db
from flask import request, make_response, jsonify
from flask_security import auth_token_required, roles_required
from datetime import datetime

from controllers.cache import cache

class StudentJobsAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        # Cache key for all active jobs
        cache_key = "student_active_jobs"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            result = cached_data
        else:
            # Get all active jobs from approved companies
            jobs = Job.query.join(Company).filter(Job.is_active == True, Company.is_approved == True).all()
            result = []
            for j in jobs:
                company = Company.query.get(j.company_id)
                result.append({
                    'id': j.id,
                    'company_name': company.company_name if company else 'Unknown',
                    'title': j.title,
                    'description': j.description,
                    'skills': j.skills,
                    'experience': j.experience,
                    'salary': j.salary,
                    'benefits': j.benefits,
                    'location': j.location,
                    'deadline': j.deadline.isoformat() if j.deadline else None,
                    'created_at': j.created_at.isoformat() if j.created_at else None
                })
            
            # Set cache for 5 minutes (300 seconds)
            cache.set(cache_key, result, timeout=300)
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class StudentApplicationsAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            return make_response(jsonify({'message': 'Please complete your profile first'}), 403)
            
        applications = Application.query.filter_by(student_id=student.id).all()
        result = []
        for app in applications:
            job = Job.query.get(app.job_id)
            company = Company.query.get(job.company_id) if job else None
            
            result.append({
                'id': app.id,
                'job_id': job.id if job else None,
                'job_title': job.title if job else 'Unknown',
                'company_name': company.company_name if company else 'Unknown',
                'status': app.status,
                'feedback': app.feedback,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'applied_at': app.applied_at.isoformat() if app.applied_at else None
            })
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class StudentJobApplyAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def post(self, job_id):
        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            return make_response(jsonify({'message': 'Please complete your profile before applying'}), 403)
            
        job = Job.query.get(job_id)
        if not job or not job.is_active:
            return make_response(jsonify({'message': 'Job not found or no longer active'}), 404)
            
        company = Company.query.get(job.company_id)
        if not company or not company.is_approved:
            return make_response(jsonify({'message': 'Company not approved yet'}), 403)
            
        # Check if already applied
        existing_app = Application.query.filter_by(student_id=student.id, job_id=job.id).first()
        if existing_app:
            return make_response(jsonify({'message': 'You have already applied for this job'}), 400)
            
        application = Application(
            student_id=student.id,
            job_id=job.id
        )
        db.session.add(application)
        db.session.commit()
        
        response = make_response(jsonify({'message': 'Successfully applied for the job!'}), 201)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response
