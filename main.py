import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fard_secret_key_2026')

# --- Firebase Initialization ---
cred_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT', 'ServiceAccountKey.json')
database_url = os.environ.get('FIREBASE_DATABASE_URL')

if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    })
else:
    print(f"Warning: Firebase service account file not found at {cred_path}")

# --- Main Routes ---

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/pillars')
def pillars():
    return render_template('pages/pillars.html')

@app.route('/transparency')
def transparency():
    return render_template('pages/transparency.html')

@app.route('/get-involved')
def get_involved():
    return render_template('pages/get_involved.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Placeholder for contact form logic
        flash("Thank you for reaching out! We will get back to you soon.", "success")
        return redirect(url_for('contact'))
    return render_template('pages/contact.html')

# --- Portals & Forms ---

@app.route('/farmer-intake', methods=['GET', 'POST'])
def farmer_intake():
    if request.method == 'POST':
        # Example of saving to Realtime Database
        if 'user_id' not in session:
            flash("Please login to submit the intake form.", "error")
            return redirect(url_for('login'))
        
        data = request.form.to_dict()
        ref = db.reference('farmer_intakes')
        ref.push({
            'user_id': session['user_id'],
            'data': data,
            'status': 'pending'
        })
        flash("Registration submitted successfully! Welcome to the FARD movement.", "success")
        return redirect(url_for('farmer_intake'))
    return render_template('portals/farmer_intake.html')

@app.route('/volunteer-form', methods=['GET', 'POST'])
def volunteer_form():
    if request.method == 'POST':
        # Placeholder for volunteer application logic
        flash("Application received! Our team will review your expertise and reach out.", "success")
        return redirect(url_for('volunteer_form'))
    return render_template('portals/volunteer_form.html')

@app.route('/partner-pitch', methods=['GET', 'POST'])
def partner_pitch():
    if request.method == 'POST':
        # Placeholder for partnership pitch logic
        flash("Pitch received! We look forward to building a sustainable future together.", "success")
        return redirect(url_for('partner_pitch'))
    return render_template('portals/partner_pitch.html')

# --- Projects & Resources ---

@app.route('/projects')
def projects():
    return render_template('projects/project_list.html')

@app.route('/projects/<project_id>')
def project_detail(project_id):
    # This would typically fetch project data from a database
    return render_template('projects/project_detail.html', project_id=project_id)

@app.route('/news')
def news():
    return render_template('blog_and_news/news_feed.html')

@app.route('/resources')
def resources():
    return render_template('resources/learning_center.html')

# --- Authentication ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Note: Firebase Admin SDK doesn't have a direct 'sign_in_with_password'
            # Typically you'd use the Client SDK on the frontend or verify ID tokens.
            # For simplicity in this demo, we verify the user exists.
            user = auth.get_user_by_email(email)
            # In a real app, password verification happens on the client or via a secure custom flow.
            session['user_id'] = user.uid
            session['email'] = user.email
            flash(f"Welcome back, {user.email}!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Login failed: {str(e)}", "error")
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

# --- Dashboards ---

@app.route('/dashboard/farmer')
def farmer_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboards/farmer/index.html')

@app.route('/dashboard/admin')
def admin_dashboard():
    # Add admin check here
    return render_template('dashboards/admin/index.html')

# --- Error Handlers ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html'), 404 # Placeholder for a proper 404 page

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html'), 500 # Placeholder for a proper 500 page

if __name__ == '__main__':
    # Professional entry point
    # Use environment variables for production configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
