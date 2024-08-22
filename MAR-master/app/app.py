from flask import flash,Flask, request, render_template, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user,current_user
import os
import json
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'raunak'
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    users = {'student': User('student', 'password'), 'faculty': User('faculty', 'password')}
    return users.get(username)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = load_user(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('submission' if username == 'student' else 'faculty'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/submission', methods=['GET', 'POST'])
@login_required
def submission():
    if request.method == 'POST':
        serial_no = request.form['serial']
        activity = request.form['activity']
        duration = request.form['duration']
        points = request.form['points']
        participated = request.form['participated']
        t_points = request.form['t_points']
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Store submission data in database
        user_dir = f'students/{current_user.username}'
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        submission_file = os.path.join(user_dir, 'submission.json')
        data = {'serial_no': serial_no, 'activity': activity, 'duration': duration, 'points': points, 'participated': participated, 't_points': t_points, 'file': filename}
        with open(f'students/{current_user.username}/submission.json', 'w') as f:
            json.dump(data, f)
        
        return 'Submission successful!'
       
    return render_template('submission.html')

# @app.route('/faculty', methods=['GET'])
# @login_required
# def faculty():
#     if current_user.username == 'faculty':
#         submissions = []
#         for student in os.listdir('students'):
#             with open(f'students/{student}/submission.json', 'r') as f:
#                 submission = json.load(f)
#                 submissions.append((student, submission))
#         return render_template('faculty.html', submissions=submissions)
#     return 'Access denied'

if not os.path.exists('students'):
    os.makedirs('students')
@app.route('/faculty', methods=['GET'])
@login_required
def faculty():
    if current_user.username == 'faculty':
        student_dirs = [d for d in os.listdir('students') if os.path.isdir(os.path.join('students', d))]
        submissions = []
        for student_dir in student_dirs:
            student_path = os.path.join('students', student_dir)
            submission_file = os.path.join(student_path, 'submission.json')
            if os.path.exists(submission_file):
                with open(submission_file, 'r') as f:
                    submission = json.load(f)
                    submissions.append((student_dir, submission))
        return render_template('faculty.html', submissions=submissions)
    return 'Access denied'

@app.route('/notify', methods=['POST'])
@login_required
def notify():
    if current_user.username == 'faculty':
        students = request.form.getlist('students')
        message = request.form['message']
        for student in students:
            send_email(student, message)
        return 'Notification sent!'
    return 'Access denied'

def send_email(student, message):
    msg = MIMEText(message)
    msg['Subject'] = 'MAR Form Reminder'
    msg['From'] = 'rkdey842@gmail.com'
    msg['To'] = f'{student}@example.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('rkdey842gmail.com', 'password')
    server.sendmail('rkdey842gmail.com', f'{student}@example.com', msg.as_string())
    server.quit()
@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    # Code to download the file
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'],'students', filename), as_attachment=True)
if __name__ == '__main__':
    app.run(port=2000,debug=True)