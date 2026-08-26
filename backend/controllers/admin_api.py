from flask_security import current_user
from controllers.models import Company, Job, Application, Student, User
from flask_restful import Resource
from controllers.database import db
from flask import request, make_response, jsonify
from flask_security import auth_token_required, roles_required
from datetime import datetime

from controllers.cache import cache

class AdminDashboardStatsAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        cache_key = "admin_dashboard_stats"
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_students': Student.query.count(),
                'total_companies': Company.query.count(),
                'total_jobs': Job.query.count(),
                'total_applications': Application.query.count()
            }
            cache.set(cache_key, stats, timeout=60)
            
        response = make_response(jsonify(stats), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class AdminCompanyManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        search_query = request.args.get('search', '')
        industry_query = request.args.get('industry', '')
        
        cache_key = f"admin_companies_{search_query}_{industry_query}"
        result = cache.get(cache_key)
        
        if result is None:
            query = Company.query
            if search_query:
                query = query.filter(Company.company_name.ilike(f'%{search_query}%'))
            if industry_query:
                query = query.filter(Company.industry.ilike(f'%{industry_query}%'))
                
            companies = query.all()
            result = []
            for c in companies:
                result.append({
                    'id': c.id,
                    'company_name': c.company_name,
                    'email': c.user.email if c.user else 'N/A',
                    'industry': c.industry,
                    'location': c.location,
                    'is_approved': c.is_approved,
                    'is_active': c.user.active if c.user else False
                })
            cache.set(cache_key, result, timeout=60)
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No data provided'}), 400)
            
        company_id = data.get('company_id')
        action = data.get('action') # 'approve', 'revoke', 'deactivate', 'activate', 'delete'
        
        company = Company.query.get(company_id)
        if not company:
            return make_response(jsonify({'message': 'Company not found'}), 404)
            
        if action == 'approve':
            company.is_approved = True
        elif action == 'revoke':
            company.is_approved = False
        elif action == 'deactivate':
            if company.user:
                company.user.active = False
        elif action == 'activate':
            if company.user:
                company.user.active = True
        elif action == 'delete':
            # This is complex due to FKs, usually better to deactivate/blacklist
            # But let's support it if needed. For now, let's stick to status.
            pass
        db.session.commit()
        cache.clear()
        
        response = make_response(jsonify({'message': f'Company updated successfully'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class AdminStudentManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        search_query = request.args.get('search', '')
        
        cache_key = f"admin_students_{search_query}"
        result = cache.get(cache_key)
        
        if result is None:
            query = Student.query
            if search_query:
                # Search by name or email (via user)
                query = query.join(User).filter(
                    (Student.full_name.ilike(f'%{search_query}%')) | 
                    (User.email.ilike(f'%{search_query}%'))
                )
                
            students = query.all()
            result = []
            for s in students:
                result.append({
                    'id': s.id,
                    'full_name': s.full_name,
                    'email': s.user.email if s.user else 'N/A',
                    'education': s.education,
                    'cgpa': s.cgpa,
                    'is_active': s.user.active if s.user else False
                })
            cache.set(cache_key, result, timeout=60)
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        student_id = data.get('student_id')
        action = data.get('action') # 'deactivate', 'activate'
        
        student = Student.query.get(student_id)
        if not student:
            return make_response(jsonify({'message': 'Student not found'}), 404)
            
        if action == 'deactivate':
            if student.user:
                student.user.active = False
        elif action == 'activate':
            if student.user:
                student.user.active = True
        db.session.commit()
        cache.clear()
        
        response = make_response(jsonify({'message': 'Student status updated'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class AdminJobManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        cache_key = "admin_all_jobs"
        result = cache.get(cache_key)
        
        if result is None:
            jobs = Job.query.all()
            result = []
            for j in jobs:
                result.append({
                    'id': j.id,
                    'title': j.title,
                    'company_name': j.company.company_name if j.company else 'N/A',
                    'is_active': j.is_active,
                    'deadline': j.deadline.isoformat() if j.deadline else None,
                    'app_count': len(j.applications)
                })
            cache.set(cache_key, result, timeout=60)
            
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        job_id = data.get('job_id')
        action = data.get('action') # 'deactivate', 'activate', 'delete'
        
        job = Job.query.get(job_id)
        if not job:
            return make_response(jsonify({'message': 'Job not found'}), 404)
            
        if action == 'deactivate':
            job.is_active = False
        elif action == 'activate':
            job.is_active = True
        elif action == 'delete':
            db.session.delete(job)
        db.session.commit()
        cache.clear()
        
        response = make_response(jsonify({'message': 'Job updated'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class AdminApplicationManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        applications = Application.query.all()
        result = []
        for a in applications:
            result.append({
                'id': a.id,
                'student_name': a.student.full_name if a.student else 'N/A',
                'company_name': a.job.company.company_name if a.job and a.job.company else 'N/A',
                'job_title': a.job.title if a.job else 'N/A',
                'status': a.status,
                'applied_at': a.applied_at.isoformat() if a.applied_at else None
            })
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class AdminPlacementManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        from controllers.models import Placement
        placements = Placement.query.all()
        result = []
        for p in placements:
            result.append({
                'id': p.id,
                'student_name': p.student.full_name if p.student else 'N/A',
                'company_name': p.company.company_name if p.company else 'N/A',
                'job_title': p.job.title if p.job else 'N/A',
                'salary': p.salary,
                'joining_date': p.joining_date.isoformat() if p.joining_date else None
            })
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response
