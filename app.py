import sqlite3
import requests
import json
from datetime import datetime
import base64
from flask import Flask, request, render_template, redirect, url_for, session, flash
from datetime import datetime
import re
from bs4 import BeautifulSoup
app = Flask(__name__)
app.secret_key = 'refooSami'  # Secret key for session management

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        number TEXT NOT NULL,
                        status TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (username) REFERENCES users(username)
                        UNIQUE(username, number, status)
                    )''')
    conn.commit()
    conn.close()

# Add a new user to the SQLite database
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('User already exists', 'danger')
    finally:
        conn.close()
# Remove a user from the SQLite database
def remove_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    cursor.execute('DELETE FROM user_data WHERE username = ?', (username,))
    conn.commit()
    conn.close()
# Authenticate user credentials
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Add data for a specific user
def add_user_data(username, number, status):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_data (username, number, status) VALUES (?, ?, ?)', (username, number, status))
    conn.commit()
    conn.close()

# Retrieve user data for a specific user
def get_user_data(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data WHERE username = ?', (username,))
    data = cursor.fetchall()
    conn.close()
    return data
# Retrieve user data by number
def get_number_data(numbers):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in numbers)
    query = f'SELECT username, number, status, timestamp FROM user_data WHERE number IN ({placeholders})'
    cursor.execute(query, numbers)
    data = cursor.fetchall()
    conn.close()
    return data
@app.route('/manage_users', methods=['GET', 'POST'])
def add_user_route():
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
                try:
                    add_user(username, password)
                    flash('User added successfully', 'success')
                except Exception as e:
                    flash(f'An error occurred: {str(e)}', 'danger')
        elif action == 'remove':
            try:
                remove_user(username)
                flash('User removed successfully', 'success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
        else:
            flash('Invalid action specified.', 'danger')

    return render_template('add_user.html')

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        search_type = request.form.get('search_type', '').strip()
        search_value = request.form.get('search_value', '').strip()

        if search_type == 'username':
            user_data = get_user_data(search_value)
            if user_data:
                total_success = sum(1 for entry in user_data if entry[3] != 'Failed')
                total_failed = sum(1 for entry in user_data if entry[3] == 'Failed')

                return render_template(
                    'user_data.html',
                    user_data=user_data,
                    search_type='username',
                    search_value=search_value,
                    total_success=total_success,
                    total_failed=total_failed
                )
            else:
                flash('No data found for the user', 'danger')

        elif search_type == 'number':
            # Allow multiple numbers, split by comma or space
            numbers = re.split(r'[,\s]+', search_value)
            number_data = get_number_data(numbers)
            if number_data:
                total_success = sum(1 for entry in number_data if entry[2] != 'Failed')
                total_failed = sum(1 for entry in number_data if entry[2] == 'Failed')

                return render_template(
                    'user_data.html',
                    number_data=number_data,
                    search_type='number',
                    search_value=search_value,
                    total_success=total_success,
                    total_failed=total_failed
                )
            else:
                flash('No data found for these numbers', 'danger')

    return render_template('user_data.html')





# Root route redirects to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            
            session['user'] = username
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('verification_code_finder'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Verification code finder route
@app.route('/verification_code_finder', methods=['GET', 'POST'])
def verification_code_finder():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if 'user' in session:
        if request.method == 'POST':
            numbers = request.form['numbers'].split()
            # phpsessid = request.form['phpsessid']
            selected_api = request.form.get('api')

            total_success = 0
            total_fail = 0
            codes = {}

            for number in numbers:
                if selected_api == '1':
                    code = get_panel_code_api1(number)
                elif selected_api == '2':
                    code = get_panel_code_api2(number)
                elif selected_api == '3':
                    code = get_panel_code_api3(number)
                elif selected_api == '4':
                    code = get_panel_code_api4(number)
                elif selected_api == '5':
                    code = get_panel_code_api5(number)
                elif selected_api == '6':
                    code = get_panel_code_api6(number)
                elif selected_api == '7':
                    code = get_panel_code_api7(number)
                elif selected_api == '8':
                    code = get_panel_code_api8(number)
                elif selected_api == '9':
                    code = get_panel_code_api9(number)
                else:
                    flash('Please select an API.', 'danger')
                    return render_template('verification.html')

                status = 'Failed'
                if code:
                    total_success += 1
                    status = code
                else:
                    total_fail += 1

                codes[number] = status
                add_user_data(session['user'], number, status)  # Save data to database

            results = {
                'total_success': total_success,
                'total_fail': total_fail,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'codes': codes
            }
            return render_template('verification.html', results=results)
        return render_template('verification.html')
    else:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))

def get_panel_code_api1(number):
    headers = {
        'Host': 'zodiacpanel.com',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://zodiacpanel.com/agent/SMSDashboard',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    response1 = requests.get('http://zodiacpanel.com/login', headers=headers)
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }
    headers = {
        'Host': 'zodiacpanel.com',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://zodiacpanel.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://zodiacpanel.com/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    data = {
        'username': 'abdo1746',
        'password': 'abdo1746',
        'capt': str(result),
    }

    response = requests.post('http://zodiacpanel.com/signin', cookies=cookies,headers=headers, data=data)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://zodiacpanel.com/agent/SMSCDRStats',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(
        f'http://zodiacpanel.com/agent/res/data_smscdr.php?fdate1=2024-10-06%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1728219621497',
        cookies=cookies,
        headers=headers,
    )
    try:
        data = json.loads(response.text)

        # Extract the message
        message_text = data['aaData'][0][5]

        verification_code = re.search(r'\d+', message_text)
            
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api2(number):
    headers = {
        'Host': '109.236.81.102',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    response1 = requests.get('http://109.236.81.102/ints/login', headers=headers)
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    cookies = {
            'PHPSESSID': response1.cookies['PHPSESSID'],
        }
    headers = {
        'Host': '109.236.81.102',
        # 'Content-Length': '54',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://109.236.81.102',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://109.236.81.102/ints/login',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',

    }

    data = {
        'username': 'abdo1746',
        'password': 'mama123123@@ASD',
        'capt': str(result),
    }

    response = requests.post('http://109.236.81.102/ints/signin', cookies=cookies, headers=headers, data=data, verify=False)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://109.236.81.102/ints/agent/SMSCDRStats',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Get the current date in the required format (YYYY-MM-DD HH:MM:SS)
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'http://109.236.81.102/ints/agent/res/data_smscdr.php?fdate1=2022-05-01%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1728052116864',
                        cookies=cookies, headers=headers)

    try:
        data = json.loads(response.text)

        # Extract the message
        message_text = data['aaData'][0][5]

        # Search for the verification code
        verification_code = re.search(r'\d+', message_text)
            
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_verification_code(number, user, password):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://45.14.135.150/ints/login', headers=headers)
    crlf = BeautifulSoup(response1.text, 'html.parser').find('input', {'name': 'crlf'})['value']
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'PHPSESSID=1q322fm42d82d7v176tpdj9cci',
        'Origin': 'http://45.14.135.150',
        'Referer': 'http://45.14.135.150/ints/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }


    data = {
        'crlf': str(crlf),
        'username': user,
        'password': password,
        'capt': str(result),
    }

    response = requests.post('http://45.14.135.150/ints/signin', cookies=cookies, headers=headers, data=data)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://45.14.135.150/ints/client/SMSCDRStats',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(
        f'http://45.14.135.150/ints/client/res/data_smscdr.php?fdate1=2024-10-09%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1728490252568',
        cookies=cookies,
        headers=headers,
    )
    try:
        data = json.loads(response.text)
        # Extract the message
        message_text = data['aaData'][0][4]

        verification_code = re.search(r'\d+', message_text)
            
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api3(number):
    code = get_verification_code(number, 'Abdo17', 'Abdo17')
    if code:
        return code

    code = get_verification_code(number, 'mohamed17450', 'mohamed4755')
    if code:
        return code
    
    code = get_verification_code(number, '1mohamed17450', 'mohamed4755')
    if code:
        return code
    code = get_verification_code(number, 'ahmedmosa1232', 'ahmedmosa1232')
    if code:
        return code
    return code

def get_verification_code2(number, user, password):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=139mjq39b8mak2ap56aiut2e26',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://45.82.67.20/ints/login', headers=headers)
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    cookies = {
            'PHPSESSID': response1.cookies['PHPSESSID'],
        }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'PHPSESSID=139mjq39b8mak2ap56aiut2e26',
        'Origin': 'http://45.82.67.20',
        'Referer': 'http://45.82.67.20/ints/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    data = {
        'username': user,
        'password': password,
        'capt': str(result),
    }

    response = requests.post('http://45.82.67.20/ints/signin', cookies=cookies, headers=headers, data=data, verify=False)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=139mjq39b8mak2ap56aiut2e26',
        'Referer': 'http://45.82.67.20/ints/agent/SMSCDRStats',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Get the current date in the required format (YYYY-MM-DD HH:MM:SS)
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'http://45.82.67.20/ints/agent/res/data_smscdr.php?fdate1=2024-10-10%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1728591594651',
                        cookies=cookies, headers=headers)

    try:
        data = json.loads(response.text)

        # Extract the message
        message_text = data['aaData'][0][5]

        # Search for the verification code
        verification_code = re.search(r'\d+', message_text)
            
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api4(number):
    code = get_verification_code2(number, 'abdo1746', 'abdo1746')
    if code:
        return code

    code = get_verification_code2(number, 'ahmedmosa19', 'ahmedmosa19')
    if code:
        return code

    return code
def get_panel_code_api5(number):
    username = 'abdo1746'
    password = 'abdo777'
    api_url = 'https://mobilink.stats.direct/rest/sms'

    # Encode the username:password combination as a Base64 string
    auth_string = f"{username}:{password}"
    auth_hash = base64.b64encode(auth_string.encode()).decode()

    # Set the headers including the Authorization header
    headers = {
        'Authorization': f'Basic {auth_hash}',
        'x-current-page': '1',
        'x-page-count': '1',
        'x-per-page': '1000',
        'x-total-count': '1000'
    }
    # Define parameters for pagination and filtering by most recent ID
    params = {
        'page': 1,        # Start at page 1
        'per-page': 1000,  # Set to maximum per page (1000)
    }
    
    # Make the request
    response = requests.get(api_url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Search for the destination_addr and get its short_message
        for record in data:
            if record.get('destination_addr') == number:
                short_message = record.get('short_message')
                # Use regex to extract the code (first sequence of 6 digits)
                code = re.search(r'\b\d{6}\b', short_message)
                if code:
                    return code.group()  # Return the extracted code
    
    # If the destination_addr wasn't found or there was an error
    return None
def get_panel_code_api6(number):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    params = {
        'key': "R1VPPUVKgHN1jVBIRVRQSEVU",
        'start': '0',
        'length': '10',
        'fnumber': number,
    }

    try:
        response = requests.post('http://pscall.net/restapi/smsreport', params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('result') == 'success' and data.get('data'):
            sms_message = data['data'][0].get('sms')
            if sms_message:
                # Extract only the digits from the message
                code = re.search(r'\d+', sms_message)
                if code:
                    return code.group(0)
        return None
    except requests.RequestException:
        return None
def get_panel_code_api7(number):
    response = requests.get(f'http://51.89.151.134/crapi/viewstats?token=%20Q1FXNEVBgmBJf5Bzd2aEW0qWUV1_VWRHZYdxa0l2YIR7l3VTVnI=&record=200&filternum={number}').json()
    if response['status'] == 'success':
        message_text = response['data'][0]['message']
        # Use a regular expression to find the digits in the message
        verification_code = re.search(r'\d+', message_text)
        
        if verification_code:
            return verification_code.group()
        else:
            return None
    else:
        return None
def get_panel_code_api8(number):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'http://93.190.143.35/ints/agent/SMSCDRReports',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://93.190.143.35/ints/', headers=headers)
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    crlf = BeautifulSoup(response1.text, 'html.parser').find('input', {'name': 'crlf'})['value']  
    cookies = {
            'PHPSESSID': response1.cookies['PHPSESSID'],
        }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://93.190.143.35',
        'Referer': 'http://93.190.143.35/ints/Login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    data = {
        'crlf': crlf,
        'username': 'abdo1746',
        'password': 'abdo1746',
        'capt': str(result),
    }

    response = requests.post('http://93.190.143.35/ints/signin', cookies=cookies, headers=headers, data=data, verify=False)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://93.190.143.35/ints/agent/SMSCDRReports',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Get the current date in the required format (YYYY-MM-DD HH:MM:SS)
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'http://93.190.143.35/ints/agent/res/data_smscdr.php?fdate1=2024-11-14%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1731622983949',
                        cookies=cookies, headers=headers)

    try:
        data = json.loads(response.text)

        # Extract the message
        message_text = data['aaData'][0][5]

        # Search for the verification code
        verification_code = re.search(r'\b\d{6}\b', message_text)
            
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
def get_panel_code_api9(number):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'http://109.236.84.81/ints/agent/SMSDashboard',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://109.236.84.81/ints/login', headers=headers)
    num1, num2 = map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num1 + num2
    cookies = {
            'PHPSESSID': response1.cookies['PHPSESSID'],
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://109.236.84.81',
        'Referer': 'http://109.236.84.81/ints/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'username': 'Abdo1746',
        'password': 'Abdo1746',
        'capt': str(result),
    }

    response = requests.post('http://109.236.84.81/ints/signin', cookies=cookies, headers=headers, data=data, verify=False)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=8hnl54gkdi25ak6h12mjpo4v3d',
    'Referer': 'http://109.236.84.81/ints/agent/SMSCDRReports',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(
        f'http://109.236.84.81/ints/agent/res/data_smscdr.php?fdate1=2024-11-21%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1732177721291',
        cookies=cookies,
        headers=headers,
    )

    try:
        data = json.loads(response.text)
        # Extract the message
        message_text = data['aaData'][0][5]
        # Search for the verification code
        verification_code = re.search(r'\b\d{6}\b', message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
