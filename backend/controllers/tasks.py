from celery import shared_task
from controllers.database import db
from controllers.models import Application, Company, Placement, Student, Job
from datetime import datetime, timedelta
import csv
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@shared_task(ignore_result=True)
def send_interview_reminders():
    # Find applications with an interview date tomorrow
    tomorrow = datetime.utcnow() + timedelta(days=1)
    # Simple check for the same date (ignoring time for simplicity in mock)
    apps = Application.query.filter(Application.interview_date != None).all()
    
    reminders_sent = 0
    for app in apps:
        if app.interview_date.date() == tomorrow.date():
            # Mock sending email/SMS/GChat
            # Example of how a webhook payload would look:
            webhook_payload = {
                "text": f"REMINDER: You have an interview scheduled tomorrow!\n\n**Company:** {app.job.company.company_name}\n**Job:** {app.job.title}\n**Date/Time:** {app.interview_date.strftime('%B %d, %Y %I:%M %p')}\n\nGood luck! - CareerLink"
            }
            requests.post("https://chat.googleapis.com/v1/spaces/AAQALbhZByI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=LBpUMuZDNm2j4Od7kdS512xD3pKy8pyPgLdTpJVIClo", json=webhook_payload)
            
            print(f"\n[REMINDER SENT - MOCK PAYLOAD: GCHAT/EMAIL]")
            print(f"To: {app.student.user.email} (Student ID: {app.student.id})")
            print(f"Content: {webhook_payload['text']}")
            reminders_sent += 1
            
    print(f"\nDaily interview reminders job complete. Sent {reminders_sent} reminders.")
    return reminders_sent

@shared_task(ignore_result=True)
def generate_monthly_placement_reports():
    # 1. Generate an HTML report for the Admin
    companies_count = Company.query.count()
    students_count = Student.query.count()
    placements_count = Placement.query.count()
    jobs_count = Job.query.count()
    applications_count = Application.query.count()
    
    html_content = f"""
    <html>
        <head><title>Monthly Placement Report</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f6f9;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">CareerLink Monthly Activity Report</h1>
                <p>Hello Admin,<br><br>Here is the automated placement activity summary for the current month:</p>
                <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px;">
                    <p><strong>Number of drives conducted:</strong> {jobs_count}</p>
                    <p><strong>Number of students applied:</strong> {applications_count}</p>
                    <p><strong>Number of students selected:</strong> {placements_count}</p>
                </div>
                <p style="margin-top: 20px; font-size: 12px; color: #7f8c8d;">Report generated on the first day of every month by CareerLink Celery Worker node.</p>
            </div>
        </body>
    </html>
    """
    
    # 2. Save the HTML Report generated
    export_dir = os.path.join(os.getcwd(), 'exports')
    os.makedirs(export_dir, exist_ok=True)
    report_path = os.path.join(export_dir, f'monthly_admin_report_{datetime.now().strftime("%Y_%m")}.html')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # 3. Simulate sending an email using smtplib (MIMEText)
    try:
        sender_email = "careerlink.noreply@institute.edu"
        receiver_email = "admin@institute.edu"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Monthly Placement Activity Report"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # --- DEMONSTRATION PURPOSES (ETHEREAL EMAIL) ---
        # 1. Go to https://ethereal.email/create to get your temporary credentials
        # 2. Replace the strings below with your Ethereal Email and Password
        ethereal_user = "bernard12@ethereal.email"
        ethereal_password = "QrkSWp9mJhdFFG1dzb"
        
        try:
            with smtplib.SMTP("smtp.ethereal.email", 587) as server:
                server.starttls() # Secure the connection
                server.login(ethereal_user, ethereal_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                
            print(f"\n[MONTHLY REPORT GENERATED]")
            print(f"HTML Report successfully saved locally to: {report_path}")
            print(f"--- ACTIVE SMTP EMAIL SEND LOG ---")
            print(f"Connected to: smtp.ethereal.email")
            print(f"To: {receiver_email}")
            print(f"Subject: {msg['Subject']}")
            print(f"Status: Email successfully sent! Check your Ethereal inbox.")
            print(f"-------------------------------------\n")
        except smtplib.SMTPAuthenticationError:
            print("\n[!] SMTP Authentication Failed!")
            print("Please make sure you replaced 'ethereal_user' and 'ethereal_password' in backend/controllers/tasks.py with your real Ethereal credentials.")
            
    except Exception as e:
        print(f"Failed to process email logic: {e}")
        
    return True

@shared_task(bind=True, ignore_result=False)
def export_applications_csv(self, user_role, user_profile_id):
    # Determine directory
    export_dir = os.path.join(os.getcwd(), 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    file_name = f"export_{user_role}_{user_profile_id}_{self.request.id}.csv"
    file_path = os.path.join(export_dir, file_name)
    
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if user_role == 'student':
                writer.writerow(['Job Title', 'Company', 'Status', 'Applied At'])
                apps = Application.query.filter_by(student_id=user_profile_id).all()
                for a in apps:
                    writer.writerow([a.job.title, a.job.company.company_name, a.status, a.applied_at])
                    
            elif user_role == 'company':
                writer.writerow(['Student Name', 'Job Title', 'Status', 'Applied At'])
                # All applications for jobs posted by this company
                apps = Application.query.join(Application.job).filter(Job.company_id==user_profile_id).all()
                for a in apps:
                    writer.writerow([a.student.full_name, a.job.title, a.status, a.applied_at])
        
        return {"status": "Complete", "file_name": file_name}
    except Exception as e:
        print(f"CSV Export Error: {e}")
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        raise e
