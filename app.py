import os
import uuid
import requests
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from panelsms_apis import *

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Global variables
stored_data = []
file_mappings = {}

# Database connection
try:
    mongo_uri = "mongodb://panelsms:Refoosami826491375@ac-o5zr4b9-shard-00-00.ottmkop.mongodb.net:27017,ac-o5zr4b9-shard-00-01.ottmkop.mongodb.net:27017,ac-o5zr4b9-shard-00-02.ottmkop.mongodb.net:27017/?replicaSet=atlas-jl9bj9-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=panelsms"
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    db = client.panelsms
    users_collection = db.users
    user_data_collection = db.user_data
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
    raise

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.active = user_data.get('active', False)
        self.registration_date = user_data.get('registration_date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_telegram_error(bot_token, chat_id, error_message):
    try:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': error_message
        }
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

# User Management Functions
def add_user(username, password):
    try:
        # Check if user already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('User already exists', 'danger')
            return False
        
        # Create new user
        user = {
            'username': username,
            'password': password,
            'created_at': datetime.now()
        }
        result = users_collection.insert_one(user)
        print(f"User added successfully with ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'danger')
        return False

def remove_user(username):
    try:
        users_collection.delete_one({'username': username})
        user_data_collection.delete_many({'username': username})
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')

def authenticate_user(username, password):
    try:
        user = users_collection.find_one({'username': username})
        if user and user['password'] == password:
            print(f"User {username} authenticated successfully")
            return True
        print(f"Authentication failed for user {username}")
        return False
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False

# User Data Functions
def add_user_data(username, number, status, api=None):
    try:
        # Check if there's an existing record with the same username, number and status (code)
        existing_entry = user_data_collection.find_one({
            'username': username,
            'number': number,
            'status': status
        })
        
        # Only add if no duplicate exists (either new number or different code)
        if not existing_entry:
            user_data = {
                'username': username,
                'number': number,
                'status': status,
                'api': api,
                'timestamp': datetime.now(),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            result = user_data_collection.insert_one(user_data)
            print(f"User data added successfully with ID: {result.inserted_id}")
            return True
        else:
            print(f"Duplicate entry found for {username}, {number}, {status} - not saving")
            return False
    except Exception as e:
        print(f"Error adding user data: {str(e)}")
        return False

def get_user_data(username):
    try:
        data = list(user_data_collection.find(
            {'username': username},
            {'_id': 0, 'username': 1, 'number': 1, 'status': 1, 'api': 1, 'date': 1}
        ).sort('timestamp', -1))
        return data
    except Exception as e:
        print(f"Error getting user data: {str(e)}")
        return []

def get_number_data(numbers):
    try:
        data = list(user_data_collection.find(
            {'number': {'$in': numbers}},
            {'_id': 0, 'username': 1, 'number': 1, 'status': 1, 'api': 1, 'date': 1}
        ).sort('timestamp', -1))
        return data
    except Exception as e:
        print(f"Error in get_number_data: {str(e)}")
        return []

# Authentication Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('verification_code_finder'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users_collection.find_one({'username': username})
        if user_data and check_password_hash(user_data['password'], password):
            if user_data.get('active', False):
                user = User(user_data)
                login_user(user)
                # Also store username in session for compatibility
                session['username'] = username
                return redirect(url_for('verification_code_finder'))
            else:
                flash('Your account is not activated yet. Please contact the administrator.', 'warning')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Clear Flask-Login authentication
    logout_user()
    
    # Clear session variables
    session.pop('username', None)
    session.clear()
    
    return redirect(url_for('login'))

@app.route('/add_user', methods=['POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists', 'danger')
            return redirect(url_for('login'))
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'password': hashed_password,
            'active': False,
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        users_collection.insert_one(user_data)
        
        flash('Account created successfully. Please wait for admin approval.', 'success')
        return redirect(url_for('login'))

# User Management Routes
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users_route():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        action = request.form.get('action', '').strip()
        
        # Validate input fields
        if not username:
            flash('Username is required.', 'danger')
        elif action == 'add':
            if not password:
                flash('Password is required for adding a user.', 'danger')
            else:
                if add_user(username, password):
                    flash('User added successfully', 'success')
        elif action == 'remove':
            try:
                remove_user(username)
                flash('User removed successfully', 'success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
        else:
            flash('Invalid action specified.', 'danger')

    return redirect(url_for('admin'))

@app.route('/activate_user', methods=['POST'])
def activate_user():
    username = request.form.get('username')
    users_collection.update_one(
        {'username': username},
        {'$set': {'active': True}}
    )
    flash(f'User {username} activated successfully', 'success')
    return redirect(url_for('admin'))

@app.route('/deactivate_user', methods=['POST'])
def deactivate_user():
    username = request.form.get('username')
    users_collection.update_one(
        {'username': username},
        {'$set': {'active': False}}
    )
    flash(f'User {username} deactivated successfully', 'warning')
    return redirect(url_for('admin'))

@app.route('/toggle_user_status', methods=['POST'])
def toggle_user_status():
    username = request.form.get('username')
    current_status = request.form.get('current_status') == 'true'
    
    # Toggle the active status
    new_status = not current_status
    
    users_collection.update_one(
        {'username': username},
        {'$set': {'active': new_status}}
    )
    
    status_text = "activated" if new_status else "deactivated"
    flash(f'User {username} {status_text} successfully', 'success' if new_status else 'warning')
    return redirect(url_for('admin'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form.get('username')
    try:
        # Use the remove_user function to ensure both user and user data are deleted
        remove_user(username)
        flash(f'User {username} and all their data deleted successfully', 'success')
    except Exception as e:
        flash(f'An error occurred while deleting user: {str(e)}', 'danger')
    return redirect(url_for('admin'))

# File Upload Routes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    # Get custom ID from form data or generate UUID
    custom_id = request.form.get('id')
    
    if custom_id and custom_id in file_mappings:
        return {'error': 'ID already exists'}, 400
    
    if file and allowed_file(file.filename):
        # Use custom ID or generate UUID
        file_id = custom_id if custom_id else str(uuid.uuid4())
        
        # Save file with original filename
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Store mapping with upload time
        file_mappings[file_id] = {
            'filename': filename,
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Return the play URL
        play_url = f"https://panelsms.onrender.com/play/{file_id}"
        return {'play_url': play_url, 'file_id': file_id}, 200
    
    return {'error': 'Invalid file type'}, 400

@app.route('/play/<file_id>')
def play_sound(file_id):
    try:
        if file_id not in file_mappings:
            return {'error': 'File ID not found'}, 404
            
        filename = file_mappings[file_id]['filename']
        return send_file(
            os.path.join(UPLOAD_FOLDER, filename),
            mimetype='audio/wav'
        )
    except FileNotFoundError:
        return {'error': 'File not found'}, 404

# API Data Routes
@app.route('/api_data', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        data = request.get_json()

        if not data or 'phone' not in data or 'code' not in data:
            return jsonify({"error": "Invalid data"}), 400

        # Save the data
        stored_data.append({"phone": data['phone'], "code": data['code']})
        print(f"📥 Stored: {data}")

        return jsonify({"message": "Data saved successfully"}), 200

    elif request.method == 'GET':
        return jsonify(stored_data), 200

# Verification Routes
@app.route('/verification_code_finder', methods=['GET', 'POST'])
def verification_code_finder():
    # Check for either Flask-Login or session-based auth
    if not current_user.is_authenticated and 'username' not in session:
        return redirect(url_for('login'))
    
    # If user is authenticated with Flask-Login but username not in session, set it
    if current_user.is_authenticated and 'username' not in session:
        session['username'] = current_user.username
    
    if request.method == 'POST':
        numbers = request.form.get('numbers')
        selected_api = request.form.get('api')
        phpsessid = request.form.get('phpsessid')
        
        if not numbers or not selected_api:
            flash('Please provide both phone numbers and API selection', 'danger')
            return render_template('dashboard/verification.html')
        
        try:
            numbers_list = [num.strip() for num in numbers.split('\n') if num.strip()]
            total_success = 0
            total_fail = 0
            codes = {}
            
            for number in numbers_list:
                code = None
                if selected_api == '+221':
                    code = get_panel_code_api1(number)
                elif selected_api == '+502':
                    code = get_panel_code_api2(number)
                elif selected_api == '+996+855':
                    code = get_panel_code_api3(number)
                elif selected_api == '+260':
                    code = get_panel_code_api4(number)
                elif selected_api == 'Kyrgyzstan':
                    code = get_panel_code_api5(number)
                elif selected_api == 'Angola':
                    code = get_panel_code_api6(number)
                elif selected_api == '+856':
                    code = get_panel_code_api7(number)
                elif selected_api == '+60':
                    code = get_panel_code_api8(number)
                elif selected_api == '+966':
                    if not phpsessid:
                        flash('PHPSESSID is required for +966 API', 'danger')
                        return render_template('dashboard/verification.html')
                    code = get_panel_code_api9(number, phpsessid)
                elif selected_api == '+31':
                    code = get_panel_code_api10(number)
                elif selected_api == 'Netherlands':
                    code = get_panel_code_api11(number)
                elif selected_api == '+507':
                    code = get_panel_code_api12(number)
                elif selected_api == '+44':
                    code = get_panel_code_api13(number)
                elif selected_api == 'Iraq':
                    if not phpsessid:
                        flash('PHPSESSID is required for Iraq API', 'danger')
                        return render_template('dashboard/verification.html')
                    code = get_panel_code_api14(number, phpsessid)
                elif selected_api == '+591':
                    code = get_panel_code_api15(number)
                elif selected_api == 'PANAMA':
                    code = get_panel_code_api16(number)
                elif selected_api == '+2':
                    code = get_panel_code_api17(number)
                elif selected_api == '+92':
                    code = get_panel_code_api18(number)
                elif selected_api == '+447':
                    code = get_panel_code_api19(number)
                elif selected_api == 'united_kingdom':
                    code = get_panel_code_api20(number)
                elif selected_api == '+93':
                    code = get_panel_code_api21(number)
                elif selected_api == '+595':
                    code = get_panel_code_api22(number)
                
                if code:
                    total_success += 1
                    status = code
                else:
                    total_fail += 1
                    status = 'Failed'
                
                codes[number] = status
                # Add data to database - will only save if it's not a duplicate
                add_user_data(session['username'], number, status, selected_api)
            
            results = {
                'total_success': total_success,
                'total_fail': total_fail,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'codes': codes
            }
            
            # Get updated user history
            user_history = get_user_data(session['username'])
            return render_template('dashboard/verification.html', results=results, user_history=user_history)
            
        except Exception as e:
            error_message = f"An error occurred:\n{str(e)}"
            send_telegram_error(
                bot_token='6893223743:AAGreuO7BRrhRcaOj8CSUKvZG1AQk-C048E',
                chat_id='854578633',
                error_message=error_message
            )
            flash('An unexpected error occurred. The admin has been notified.', 'danger')
            return render_template('dashboard/verification.html')
    
    # Get user history for the history tab
    user_history = get_user_data(session['username'])
    return render_template('dashboard/verification.html', user_history=user_history)

# Admin Routes
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Get all users for the user management tab
    all_users = list(users_collection.find({}, {'_id': 0, 'username': 1, 'active': 1, 'registration_date': 1}))
    
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_value = request.form.get('search_value')
        
        if not search_value:
            flash('Please enter a search value', 'danger')
            return render_template('dashboard/admin.html', all_users=all_users)
        
        try:
            if search_type == 'username':
                user_data = get_user_data(search_value)
                if user_data:
                    total_success = sum(1 for entry in user_data if entry['status'] != 'Failed')
                    total_failed = sum(1 for entry in user_data if entry['status'] == 'Failed')
                    
                    return render_template(
                        'dashboard/admin.html',
                        user_data=user_data,
                        total_success=total_success,
                        total_failed=total_failed,
                        search_type=search_type,
                        search_value=search_value,
                        all_users=all_users
                    )
                else:
                    flash('No data found for the specified username', 'info')
            
            elif search_type == 'number':
                number_data = get_number_data([search_value])
                if number_data:
                    total_success = sum(1 for entry in number_data if entry['status'] != 'Failed')
                    total_failed = sum(1 for entry in number_data if entry['status'] == 'Failed')
                    
                    return render_template(
                        'dashboard/admin.html',
                        user_data=number_data,
                        total_success=total_success,
                        total_failed=total_failed,
                        search_type=search_type,
                        search_value=search_value,
                        all_users=all_users
                    )
                else:
                    flash('No data found for the specified number', 'info')
            
            else:
                flash('Invalid search type', 'danger')
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            flash('An error occurred during search', 'danger')
    
    return render_template('dashboard/admin.html', all_users=all_users)

# Main entry point
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)