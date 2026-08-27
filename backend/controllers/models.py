from controllers.database import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin


# =========================
# USER TABLE
# =========================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Flask-Security Role Relationship
    roles = db.relationship(
        'Role',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic')
    )

    # One-to-One Relationships
    student_profile = db.relationship("Student", backref="user", uselist=False)
    company_profile = db.relationship("Company", backref="user", uselist=False)


# =========================
# ROLE TABLE
# =========================
class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# =========================
# USER-ROLE ASSOCIATION
# =========================
class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


# =========================
# COMPANY TABLE
# =========================
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    company_name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One Company → Many Jobs
    jobs = db.relationship("Job", backref="company", lazy=True)

    # One Company → Many Placements
    placements = db.relationship("Placement", backref="company", lazy=True)


# =========================
# STUDENT TABLE
# =========================
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    full_name = db.Column(db.String(255), nullable=False)
    education = db.Column(db.String(255))
    cgpa = db.Column(db.Float)
    skills = db.Column(db.Text)
    experience = db.Column(db.String(255))
    resume_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One Student → Many Applications
    applications = db.relationship("Application", backref="student", lazy=True)

    # One Student → One Placement
    placement = db.relationship("Placement", backref="student", uselist=False)


# =========================
# JOB TABLE
# =========================
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(255))
    experience = db.Column(db.String(255))
    salary = db.Column(db.String(100))
    benefits = db.Column(db.Text)
    location = db.Column(db.String(255))
    deadline = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One Job → Many Applications
    applications = db.relationship("Application", backref="job", lazy=True)
    placements = db.relationship("Placement", backref="job", lazy=True)


# =========================
# APPLICATION TABLE
# =========================
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    status = db.Column(db.String(50), default='Applied')
    feedback = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One Application → Optional Placement
    placement = db.relationship("Placement", backref="application", uselist=False)


# =========================
# PLACEMENT TABLE
# =========================
class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))

    salary = db.Column(db.String(100))
    joining_date = db.Column(db.DateTime)