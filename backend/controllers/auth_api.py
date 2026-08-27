from flask_security import current_user

from controllers.models import User, Company, Job, Application, Placement, Student
from controllers.user_datastore import user_datastore
from flask_restful import Resource
from controllers.database import db
from flask import request,make_response,jsonify
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin, utils, auth_token_required,roles_required

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data: 
            result={
                'message': 'No data provided' 
                }
            return make_response(jsonify(result), 400)



        email = data.get('email',None)
        password = data.get('password',None)
        if not email or not password:
            result={
                'message': 'Email and password are required' 
                }
            return make_response(jsonify(result), 400)



        user = user_datastore.find_user(email=email)
        if not user:
            result={
                'message': 'User not found' 
                }
            return make_response(jsonify(result), 404)

        if not utils.verify_password(password, user.password):
            result={
                'message': 'Invalid credentials' 
                }
            return make_response(jsonify(result), 401)


        utils.login_user(user)

        token = user.get_auth_token()

        result={
            'message': 'Login successful',
            'token': token,
            'user_details':{
                'id': user.id,
                'email': user.email,
                'roles': [role.name for role in user.roles],

            }
        }
        return make_response(jsonify(result), 200)
    


class check_email_availabilityAPI(Resource):
    def post (self):
        data = request.get_json()
        if not data:
            result={
                'message': 'No data provided' 
                }
            return make_response(jsonify(result), 400)
        email= data.get('email',None)
        if not email:
            result={
                'message': 'Email is required' 
                }
            return make_response(jsonify(result), 400)
        user=user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'available': False}), 200)
        else:
            return make_response(jsonify({'available': True}), 200)
            
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        result={
            'message': 'Logout successful'
        }
        return make_response(jsonify(result), 200)
    

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data: 
            result={
                'message': 'No data provided' 
                }
            return make_response(jsonify(result), 400)

        email = data.get('email',None)
        password = data.get('password',None)
        role = data.get('role',None)

        if not email or not password or not role:
            result={
                'message': 'Email, password and role are required' 
                }
            return make_response(jsonify(result), 400)
        
        if "@" not in email:
            result={
                'message': 'Invalid email format' 
                }
            return make_response(jsonify(result), 400)

        if user_datastore.find_user(email=email):
            result={
                'message': 'User already exists' 
                }
            return make_response(jsonify(result), 409)

        user_datastore.create_user(email=email, password=utils.hash_password(password), roles=[role])
        db.session.commit()

        result={
            'message': 'User registered successfully',
            'user_details':{
                'email': email,
                'role': role
            }
        }
        return make_response(jsonify(result), 201)

# Admin_DashAPI moved to admin_api.py as AdminDashboardStatsAPI
    

class Student_DashAPI(Resource):
    # display user dashboard
    @auth_token_required
    @roles_required('student')
    def get(self):
        user = current_user
        result = {
            'email': user.email,
            'roles': [role.name for role in user.roles]
        }
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class StudentProfileAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()
        
        result = {}
        if student:
            result = {
                'full_name': student.full_name,
                'education': student.education,
                'cgpa': student.cgpa,
                'skills': student.skills,
                'experience': student.experience,
                'resume_filename': student.resume_filename
            }
        
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('student')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No data provided'}), 400)

        user = current_user
        student = Student.query.filter_by(user_id=user.id).first()

        full_name = data.get('full_name')
        if not full_name:
            return make_response(jsonify({'message': 'Full name is required'}), 400)

        if not student:
            student = Student(user_id=user.id, full_name=full_name)
            db.session.add(student)
        else:
            student.full_name = full_name

        student.education = data.get('education')
        
        # safely parse float
        cgpa_val = data.get('cgpa')
        if cgpa_val:
            try:
                student.cgpa = float(cgpa_val)
            except ValueError:
                student.cgpa = None
        else:
            student.cgpa = None

        student.skills = data.get('skills')
        student.experience = data.get('experience')
        student.resume_filename = data.get('resume_filename')

        db.session.commit()

        response = make_response(jsonify({'message': 'Profile updated successfully'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class Company_DashAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        result = {
            'email': user.email,
            'roles': [role.name for role in user.roles],
            'is_approved': company.is_approved if company else False
        }
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

class CompanyProfileAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self):
        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()
        
        result = {}
        if company:
            result = {
                'company_name': company.company_name,
                'industry': company.industry,
                'location': company.location,
                'description': company.description
            }
        
        response = make_response(jsonify(result), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

    @auth_token_required
    @roles_required('company')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No data provided'}), 400)

        user = current_user
        company = Company.query.filter_by(user_id=user.id).first()

        company_name = data.get('company_name')
        if not company_name:
            return make_response(jsonify({'message': 'Company name is required'}), 400)

        if not company:
            company = Company(user_id=user.id, company_name=company_name)
            db.session.add(company)
        else:
            company.company_name = company_name

        company.industry = data.get('industry')
        company.location = data.get('location')
        company.description = data.get('description')

        db.session.commit()

        response = make_response(jsonify({'message': 'Company Profile updated successfully'}), 200)
        response.headers['Authentication-Token'] = current_user.get_auth_token()
        return response

# Admin related APIs moved to admin_api.py