# CareerLink

## Overview



CareerLink is a modern **Placement Portal Application (PPA)** designed to digitize and streamline campus recruitment activities involving students, companies, and administrators.

The platform provides a centralized system for managing:

* Student profiles
* Company registration and approval
* Placement drives
* Job listings
* Student applications
* Application status tracking
* Placement records
* Administrative management
* CSV data exports
* Background processing and scheduled tasks

The project follows a separated **frontend and backend architecture**, providing a scalable structure with a RESTful backend API and a reactive Single Page Application frontend.

The system supports three major user roles:

* **Admin**
* **Student**
* **Company**

The backend is implemented using Flask and Flask-RESTful, while the frontend is developed using Vue.js 3 and Vite. Redis and Celery are used for caching and asynchronous background processing.

---

## 🚀 Project Overview

CareerLink acts as a centralized bridge between educational institutions, students, and recruiting companies.

The platform digitizes the traditional placement process by allowing:

### 🎓 Students

* Create and manage academic profiles
* Browse active placement drives
* Apply for jobs
* Track application status
* View placement-related information

### 🏢 Companies

* Maintain company profiles
* Create placement drives
* Publish job opportunities
* View applicants
* Process applications
* Shortlist or reject candidates

### 👨‍💼 Administrators

* Manage students
* Manage companies
* Approve or revoke companies
* Moderate placement drives
* Monitor system statistics
* Manage overall placement activity

---

## 🎯 Problem Statement

Institutes often require efficient systems to manage campus recruitment activities involving companies and students.

Traditional placement management can involve multiple disconnected processes for:

* Company approvals
* Student registration
* Placement drive creation
* Job applications
* Application status tracking
* Placement records
* Administrative monitoring

CareerLink addresses these challenges by providing a centralized Placement Portal Application that digitizes and streamlines the complete recruitment workflow.

The primary objective is to make placement management more organized, efficient, scalable, and easier to monitor.

---

# 🎯 Objectives

The main objectives of CareerLink are:

* Digitize campus placement activities
* Provide role-based access for Admin, Student, and Company users
* Secure the application using token-based authentication
* Allow companies to manage placement drives
* Allow students to discover and apply for opportunities
* Track application status throughout the recruitment lifecycle
* Maintain historical placement information
* Provide administrative monitoring and management
* Support background processing for heavy tasks
* Improve API performance through caching
* Generate application data exports
* Provide a scalable frontend-backend architecture

---

# 🏗️ System Architecture

CareerLink follows a separated frontend and backend architecture.

```text
                         CareerLink
                              |
                +-------------+-------------+
                |                           |
                v                           v
          Vue.js 3 Frontend          Flask Backend API
                |                           |
                |                    Flask-RESTful
                |                           |
                |                    Authentication
                |                           |
                |                    Flask-Security-Too
                |                           |
                |                    Flask-SQLAlchemy
                |                           |
                |                           v
                |                       SQLite
                |
                +---------------------------+
                            |
                            v
                       Redis / Celery
                            |
                 +----------+----------+
                 |                     |
                 v                     v
          Background Tasks       Caching
                 |
                 v
          CSV Export / Emails
```

The frontend and backend are separated to maintain clear separation of concerns and support scalability.

---

# 🛠️ Technology Stack

| Category             | Technology                  |
| -------------------- | --------------------------- |
| Programming Language | Python 3                    |
| Backend Framework    | Flask                       |
| REST API             | Flask-RESTful               |
| CORS                 | Flask-CORS                  |
| Database             | SQLite 3                    |
| ORM                  | Flask-SQLAlchemy            |
| Authentication       | Flask-Security-Too          |
| Authentication Type  | Token-based Authentication  |
| Frontend             | Vue.js 3                    |
| Frontend API         | Composition API             |
| Bundler              | Vite                        |
| Routing              | Vue Router                  |
| Styling              | Native CSS, Bootstrap       |
| Task Queue           | Celery                      |
| Task Scheduling      | Celery Beat                 |
| Message Broker       | Redis                       |
| Caching              | Redis, Flask-Caching        |
| PDF Generation       | FPDF                        |
| Data Export          | Python CSV Standard Library |
| Version Control      | Git / GitHub                |

The technology stack is based directly on the project implementation described in the project report.

---

# 👥 User Roles

CareerLink provides three primary roles.

## 👨‍💼 Admin

Administrators have centralized control over the placement portal.

### Admin capabilities

* View dashboard statistics
* Browse students
* Manage student access
* Browse companies
* Approve companies
* Revoke company approval
* Moderate placement drives
* Monitor overall system activity

---

## 🎓 Student

Students can use CareerLink to discover and apply for placement opportunities.

### Student capabilities

* Register and authenticate
* Manage personal and academic profile
* View active placement drives
* Apply for placement opportunities
* View submitted applications
* Track application status

Application statuses include:

* Applied
* Shortlisted
* Selected
* Rejected

---

## 🏢 Company

Companies can use CareerLink to manage their recruitment activities.

### Company capabilities

* Register and authenticate
* Manage company profile
* Create placement drives
* Update placement drives
* View applicants
* Process applications
* Shortlist candidates
* Reject candidates

---

# 🔐 Authentication & Security

CareerLink uses **Flask-Security-Too** for token-based authentication.

The API uses the:

```text
Authentication-Token
```

header to secure protected endpoints.

Authentication includes:

```text
Register
   |
   v
Login
   |
   v
Authentication Token
   |
   v
Protected API Endpoints
```

The system supports role-based access for:

* Admin
* Student
* Company

This ensures that users can access functionality appropriate to their assigned role.

---

# 🗄️ Database Design

The CareerLink database revolves around several interconnected entities.

## User

The base authentication entity containing information such as:

* ID
* Email
* Password
* Active status

## Role & RolesUsers

These entities support role assignment and allow users to be associated with:

* Admin
* Student
* Company

## Student

The Student entity has a one-to-one relationship with User.

It stores academic information such as:

* Full name
* CGPA
* Education

## Company

The Company entity also has a one-to-one relationship with User.

It stores:

* Company name
* Industry
* Location
* Approval status

## Job

The Job entity represents a placement drive.

It stores:

* Title
* Description
* Skills
* Salary
* Deadline
* Active status

Each job is associated with a company.

## Application

Application acts as the connection between Students and Jobs.

It records:

* Student
* Job
* Application status
* Application timestamp

Possible statuses include:

```text
Applied
   |
   +----> Shortlisted
   |
   +----> Rejected
   |
   +----> Selected
```

## Placement

The Placement entity maintains historical records of students who were hired by companies through specific jobs.

The database entities and relationships are described in the project report.

---

# 🔄 Placement Workflow

The overall placement workflow can be represented as:

```text
                    Company Registration
                            |
                            v
                    Admin Approval
                            |
                            v
                  Company Creates Job
                            |
                            v
                    Placement Drive
                            |
                            v
                    Student Views Job
                            |
                            v
                    Student Applies
                            |
                            v
                    Company Reviews
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
         Shortlisted    Rejected      Selected
              |                           |
              |                           v
              |                       Placement
              |                           |
              +-------------+-------------+
                            |
                            v
                    Application Tracking
```

This workflow allows the platform to track the lifecycle of an application from initial submission through selection or rejection.

---

# 🔌 REST API

The CareerLink REST API is prefixed with:

```text
/api
```

Protected endpoints use the `Authentication-Token` header.

---

## 🔐 Authentication Endpoints

| Method | Endpoint    | Description                                       |
| ------ | ----------- | ------------------------------------------------- |
| POST   | `/register` | Register a new Student or Company                 |
| POST   | `/login`    | Authenticate user and return authentication token |

---

## 🎓 Student Endpoints

| Method | Endpoint                | Description                       |
| ------ | ----------------------- | --------------------------------- |
| GET    | `/student/profile`      | Retrieve student profile          |
| PUT    | `/student/profile`      | Update student profile            |
| GET    | `/student/jobs`         | Fetch active placement drives     |
| GET    | `/student/applications` | View applications                 |
| POST   | `/student/applications` | Apply for a placement opportunity |

The student job listing endpoint uses cached active placement-drive data according to the project architecture.

---

## 🏢 Company Endpoints

| Method | Endpoint                      | Description                   |
| ------ | ----------------------------- | ----------------------------- |
| GET    | `/company/profile`            | Retrieve company profile      |
| PUT    | `/company/profile`            | Update company profile        |
| GET    | `/company/jobs`               | View company placement drives |
| POST   | `/company/jobs`               | Create placement drive        |
| PUT    | `/company/jobs/`              | Update placement drive        |
| GET    | `/company/jobs//applications` | View applicants               |
| PUT    | `/company/applications/`      | Process applications          |

These endpoints allow companies to manage placement drives and process applicants.

---

## 👨‍💼 Admin Endpoints

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| GET    | `/admin/dashboard` | View system statistics    |
| GET    | `/admin/companies` | Browse companies          |
| POST   | `/admin/companies` | Manage company approval   |
| GET    | `/admin/students`  | Browse students           |
| POST   | `/admin/students`  | Manage student access     |
| GET    | `/admin/jobs`      | Browse placement drives   |
| POST   | `/admin/jobs`      | Moderate placement drives |

The dashboard and selected API endpoints use caching for frequently accessed information.

---

# ⚡ Asynchronous Processing

CareerLink uses **Celery** and **Redis** to move heavy or scheduled operations away from the main Flask web server.

This architecture is useful for operations such as:

* CSV data generation
* Batch email reminders
* Scheduled background tasks

The task queue uses Redis as the message broker.

---

# 📊 Caching & Performance

Redis and Flask-Caching are used to improve application performance.

Frequently accessed API resources can be cached instead of repeatedly querying the database.

Examples include:

* Job listings
* Dashboard statistics

This reduces unnecessary database operations and improves response times for frequently requested information.

---

# 📤 Export System

CareerLink includes an asynchronous export system for generating application data.

The export workflow is:

```text
POST /export
      |
      v
Celery Background Job
      |
      v
Generate CSV Data
      |
      v
Check Job Status
      |
      v
Download Generated File
```

### Export Endpoints

| Method | Endpoint            | Description                 |
| ------ | ------------------- | --------------------------- |
| POST   | `/export`           | Submit CSV export task      |
| GET    | `/export/status/`   | Check background job status |
| GET    | `/export/download/` | Download generated file     |

The export operation is processed as a Celery batch task rather than blocking the main web server.

---

# 📄 Report & PDF Generation

The project includes support for report/PDF generation using:

```text
FPDF
```

CSV exports use Python's standard CSV library.

This allows placement-related data to be transformed into downloadable reports and structured datasets.

---

# 🎨 Frontend

The CareerLink frontend is built using:

* Vue.js 3
* Composition API
* Vite
* Vue Router
* Native CSS
* Bootstrap

The Vue.js Single Page Application provides:

* Reactive user interfaces
* Client-side routing
* Dynamic forms
* Dashboard navigation
* Role-specific interfaces

The frontend communicates with the Flask REST API to perform application operations.

---

# 🖥️ Backend

The backend is implemented using:

* Python 3
* Flask
* Flask-RESTful
* Flask-CORS
* Flask-SQLAlchemy
* Flask-Security-Too

The backend provides RESTful API endpoints for:

* Authentication
* Student management
* Company management
* Job management
* Applications
* Placements
* Administration
* Data exports

Database access is abstracted through Flask-SQLAlchemy ORM.

---

# 🧩 Project Architecture

```text
CareerLink
│
├── Frontend
│   ├── Vue.js 3
│   ├── Composition API
│   ├── Vue Router
│   ├── Vite
│   ├── Bootstrap
│   └── Native CSS
│
├── Backend
│   ├── Python 3
│   ├── Flask
│   ├── Flask-RESTful
│   ├── Flask-CORS
│   ├── Flask-SQLAlchemy
│   └── Flask-Security-Too
│
├── Database
│   └── SQLite 3
│
├── Background Processing
│   ├── Celery
│   └── Celery Beat
│
├── Broker & Cache
│   ├── Redis
│   └── Flask-Caching
│
└── Reports & Export
    ├── FPDF
    └── CSV
```

---

# 🔄 End-to-End Workflow

```text
                         CAREERLINK
                              |
                              v
                     User Authentication
                              |
                 +------------+------------+
                 |            |            |
                 v            v            v
              Admin        Student      Company
                 |            |            |
                 |            v            |
                 |      Browse Jobs        |
                 |            |            v
                 |            |       Create Jobs
                 |            |            |
                 |            v            |
                 |       Apply for Job <---+
                 |            |
                 |            v
                 |      Application
                 |        Tracking
                 |            |
                 |            v
                 |        Selection
                 |            |
                 +------------+
                              |
                              v
                         Placement
                              |
                              v
                    Historical Records
```

---

# 📈 Performance Architecture

CareerLink uses multiple techniques to improve application performance and scalability.

### REST API

Flask-RESTful provides a structured API layer between the frontend and backend.

### ORM

Flask-SQLAlchemy provides abstraction over database operations.

### Caching

Redis and Flask-Caching reduce repeated database queries for frequently accessed information.

### Background Tasks

Celery allows resource-intensive operations to run asynchronously.

### Scheduled Tasks

Celery Beat supports scheduled operations such as recurring background jobs.

This architecture separates user-facing request processing from computationally heavier background work.

---

# 🔐 Security Architecture

The project uses token-based authentication through Flask-Security-Too.

```text
User
 |
 v
Login
 |
 v
Authentication Token
 |
 v
Authentication-Token Header
 |
 v
Protected REST API
 |
 v
Role-Based Access
 |
 +----> Admin
 |
 +----> Student
 |
 +----> Company
```

This provides controlled access to role-specific resources and API operations.

---

# 📚 Core Database Relationships

```text
                 User
                  |
          +-------+-------+
          |       |       |
          v       v       v
       Student  Company   Role
          |        |
          |        v
          |       Job
          |        |
          |        |
          +------> Application
                     |
                     v
                 Placement
```

### Relationship Summary

| Entity                | Relationship      |
| --------------------- | ----------------- |
| User → Student        | One-to-One        |
| User → Company        | One-to-One        |
| User → Role           | Role assignment   |
| Company → Job         | Many-to-One       |
| Student → Application | One-to-Many       |
| Job → Application     | One-to-Many       |
| Student → Placement   | Placement history |
| Company → Placement   | Placement history |
| Job → Placement       | Placement history |

The core entity relationships are based on the database design described in the project report.

---

# 🧪 Key Functional Areas

CareerLink covers the following functional areas:

| Module                 | Functionality                           |
| ---------------------- | --------------------------------------- |
| Authentication         | Registration and login                  |
| Authorization          | Role-based access                       |
| Student Management     | Academic profile management             |
| Company Management     | Company profile management              |
| Job Management         | Placement drive creation and management |
| Application Management | Job applications and status tracking    |
| Placement Management   | Historical placement records            |
| Administration         | Platform-level management               |
| Caching                | Faster access to frequently used data   |
| Background Tasks       | Asynchronous processing                 |
| Export                 | Application CSV generation              |
| Reports                | PDF/report generation                   |

---

# 💡 Key Features

## 🎓 Student Features

* Student registration
* Secure authentication
* Academic profile management
* Placement drive discovery
* Job applications
* Application status tracking
* Placement information

## 🏢 Company Features

* Company registration
* Company approval workflow
* Company profile management
* Placement drive creation
* Placement drive updates
* Applicant management
* Application processing

## 👨‍💼 Admin Features

* Dashboard statistics
* Company management
* Company approval/revocation
* Student management
* Student access management
* Job moderation

## ⚙️ System Features

* RESTful API
* Token-based authentication
* Role-based access
* Redis caching
* Celery background tasks
* Celery Beat scheduling
* CSV exports
* PDF/report generation

---

# 📊 Project Workflow Summary

```text
                 User Registration
                        |
                        v
                 Authentication
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        Admin        Student       Company
          |             |             |
          |             v             |
          |        Browse Jobs        |
          |             |             v
          |             |       Create Placement
          |             |             |
          |             v             |
          |          Apply <----------+
          |             |
          |             v
          |       Application Review
          |             |
          |       +-----+-----+
          |       |           |
          |       v           v
          |   Shortlisted   Rejected
          |       |
          |       v
          |    Selected
          |       |
          |       v
          |   Placement
          |
          v
      Administration
          |
          v
   Dashboard / Reports
```

---

# 🚀 Scalability & Performance

The application architecture was designed with scalability in mind.

The separation of frontend and backend allows each component to evolve independently.

Performance improvements include:

* Redis-based caching
* Flask-Caching
* Asynchronous Celery tasks
* Redis message broker
* Scheduled background operations
* ORM-based database abstraction

Frequently accessed resources such as job listings and dashboard statistics can be cached, while expensive operations such as CSV generation are handled asynchronously.

---

# 📁 Project Components

The project is organized around the following major components:

```text
CareerLink
│
├── Backend
│   ├── REST API
│   ├── Authentication
│   ├── Database Models
│   ├── Business Logic
│   └── Background Tasks
│
├── Frontend
│   ├── Vue Components
│   ├── Dashboards
│   ├── Forms
│   └── Routing
│
├── Database
│   └── SQLite
│
├── Cache / Broker
│   └── Redis
│
└── Reports / Exports
    ├── CSV
    └── PDF
```

---

# 🧰 Development Tools

The project uses the following development technologies:

* Python 3
* Flask
* Flask-RESTful
* Flask-SQLAlchemy
* Flask-Security-Too
* Vue.js 3
* Vite
* Vue Router
* Bootstrap
* Celery
* Celery Beat
* Redis
* Flask-Caching
* FPDF
* Git
* GitHub

---

# 📌 API Design Summary

CareerLink follows a REST-oriented API design.

```text
/api
│
├── Authentication
│   ├── /register
│   └── /login
│
├── Student
│   ├── /student/profile
│   ├── /student/jobs
│   └── /student/applications
│
├── Company
│   ├── /company/profile
│   ├── /company/jobs
│   └── /company/applications
│
├── Admin
│   ├── /admin/dashboard
│   ├── /admin/companies
│   ├── /admin/students
│   └── /admin/jobs
│
└── Export
    ├── /export
    ├── /export/status/
    └── /export/download/
```

---

# 🤖 AI/LLM Usage

AI tools were used as development assistance during the project.

According to the project declaration, ChatGPT was used for:

* SQLAlchemy model definition assistance
* API documentation examples
* Variable naming consistency
* Documentation formatting

The reported AI/LLM usage was approximately **15–20%**, limited primarily to code suggestions and documentation assistance.

The final implementation logic, debugging, and integration were completed manually.

---

# 🎥 Project Presentation

A project presentation video is included/referenced in the project report as:

```text
CareerLink Demo.mp4
```

The report identifies this as the project's video presentation.

---

# 🔮 Future Improvements

Potential future improvements for CareerLink include:

* Advanced student skill matching
* Automated candidate ranking
* AI-powered job recommendations
* Resume parsing
* Resume-to-job matching
* Advanced placement analytics
* Company-wise placement statistics
* Student performance analytics
* Email notification improvements
* Real-time notifications
* PostgreSQL support for larger deployments
* Containerized deployment using Docker
* Cloud deployment
* Advanced monitoring and logging
* More comprehensive automated testing

These are proposed future enhancements and are not claimed as currently implemented features.

---

# ⚠️ Limitations

The current project architecture has some areas that could be extended for production-scale deployment.

### Database

The project uses SQLite, which is suitable for development and smaller deployments but could be replaced with a production-grade relational database for larger workloads.

### Analytics

The current system focuses primarily on placement management and tracking. More advanced analytics could be added in future versions.

### Recommendation Engine

The current architecture does not document an AI-based recommendation engine. Intelligent student-job matching could be introduced as a future enhancement.

### Testing

Additional automated unit, integration, and end-to-end testing could strengthen the system.

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

* Full-stack web development
* REST API development
* Role-based authentication
* Database modeling
* Object-relational mapping
* Frontend-backend integration
* Asynchronous task processing
* Task scheduling
* Redis caching
* API design
* Data export
* PDF generation
* Software architecture
* Git and GitHub based development

---

# 📌 Key Takeaways

### 1. Role-Based Placement Management

CareerLink provides separate workflows for Admin, Student, and Company users.

### 2. RESTful Backend

The Flask backend provides structured API endpoints for authentication, profiles, jobs, applications, administration, and exports.

### 3. Reactive Frontend

Vue.js 3 provides a modern Single Page Application experience.

### 4. Asynchronous Processing

Celery and Redis prevent resource-intensive background operations from blocking the main web server.

### 5. Performance Optimization

Redis and Flask-Caching improve performance for frequently accessed resources.

### 6. Application Lifecycle Tracking

Applications can progress through:

```text
Applied → Shortlisted → Selected
                      ↘
                       Rejected
```

### 7. Centralized Placement Records

The Placement entity provides historical tracking of successful student-company-job relationships.

---

# 📊 Feature Summary

| Feature              | Status      |
| -------------------- | ----------- |
| Student Registration | Implemented |
| Company Registration | Implemented |
| Admin Management     | Implemented |
| Token Authentication | Implemented |
| Role-Based Access    | Implemented |
| Student Profiles     | Implemented |
| Company Profiles     | Implemented |
| Placement Drives     | Implemented |
| Job Applications     | Implemented |
| Application Status   | Implemented |
| Placement Tracking   | Implemented |
| REST API             | Implemented |
| Redis Caching        | Implemented |
| Celery Tasks         | Implemented |
| Celery Beat          | Implemented |
| CSV Export           | Implemented |
| PDF Generation       | Implemented |

---

# 🏁 Conclusion

CareerLink demonstrates the development of a complete **Placement Portal Application** designed to streamline campus recruitment activities.

The project combines a Flask RESTful backend with a Vue.js 3 Single Page Application and integrates SQLite, Flask-SQLAlchemy, Flask-Security-Too, Redis, Flask-Caching, Celery, and Celery Beat.

The system provides dedicated workflows for **Administrators, Students, and Companies**, allowing the complete placement process to be managed through a centralized platform.

From company approval and placement-drive creation to student applications, application status tracking, and placement history, CareerLink provides an end-to-end digital workflow for campus recruitment.

The use of asynchronous processing and caching additionally demonstrates practical considerations for application performance and scalability.

Overall, CareerLink demonstrates practical knowledge of **full-stack development, REST API design, authentication, database architecture, asynchronous processing, caching, and modern frontend development**.

---

# 👨‍💻 Author

**Bhushan Dattatray Sonawane**

**Roll No.:** 23f2003210

**Program:** BS Degree in Data Science and Applications

**Institute:** IIT Madras

**Project:** CareerLink – Placement Portal Application

**Focus:** Full-Stack Web Development, REST APIs, Database Systems, Authentication & Scalable Application Architecture

---

## 📜 Project Declaration

This project was developed as an academic project to design and implement a modern placement portal capable of managing interactions between students, companies, and administrators.

The implementation combines modern frontend and backend technologies with database management, authentication, caching, asynchronous processing, and data export capabilities.
