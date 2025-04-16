
import requests
import json
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import base64
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
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'http://94.23.120.156/ints/agent/SMSCDRReports',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://94.23.120.156/ints/login', headers=headers)
    num1, num2, num3= map(int, re.findall(r'\d+', BeautifulSoup(response1.text, 'html.parser').get_text()))
    result = num2 + num3

    cookies = {
            'PHPSESSID': response1.cookies['PHPSESSID'],
        }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://94.23.120.156',
        'Referer': 'http://94.23.120.156/ints/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    data = {
        'username': 'Abdo17461746',
        'password': 'welcome123',
        'capt': str(result),
    }

    response2 = requests.post('http://94.23.120.156/ints/signin', cookies=cookies, headers=headers, data=data)

    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://94.23.120.156/ints/agent/SMSCDRReports',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Get the current date in the required format (YYYY-MM-DD HH:MM:SS)
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'http://94.23.120.156/ints/agent/res/data_smscdr.php?fdate1=2025-04-14%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=2&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch={number}&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1744636782383',
                        cookies=cookies, headers=headers)

    try:
        data = json.loads(response.text)

        # Extract the message
        message_text = data['aaData'][0][5]
        print(message_text)
        # Search for any 5-6 digit verification code in the message
        verification_code = re.search(r'(?<!\d)\d{5,6}(?!\d)', message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
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

    response2 = requests.post('http://93.190.143.35/ints/signin', cookies=cookies, headers=headers, data=data)
    

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
def get_panel_code_api9(number,phpsessid):
    cookies = {
        'PHPSESSID': phpsessid,
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
        timeout=30
    )

    try:
        data = json.loads(response.text)
        # Extract the message
        message_text = data['aaData'][0][5]
        # Search for the verification code
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api10(number):
    code = get_verification_code3(number, 'abdomostafa1746', 'abdomostafa1746')
    if code:
        return code

    code = get_verification_code3(number, 'abdo1746', 'abdo1746')
    if code:
        return code

    return code  
def get_panel_code_api11(number):
    code = get_verification_code4(number, 'Abdo17461746', 'Abdo17461746')
    if code:
        return code

    code = get_verification_code4(number, 'mohhhamd01', 'mohhhamd0')
    if code:
        return code

    return code  
def get_panel_code_api12(number):
    def get_ip():
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print("Failed to fetch IP address:", e)
            return None

    # Map of IP addresses to tokens
    ip_token_map = {
        '52.15.118.168': 'HUS83ojxYHmsXyJPb0XUui9p5FY3V2pNPdoN6TBK47f19650',
        '3.129.111.220': 'kbEKtRHGNbGXJrjSs02D5jk27GWJNcLAjZwDm7mdb3eebafc',
        '3.134.238.10': 'tqimpuIULab9dtcbRssavrhuShijdNupBzjhNnxa62d80b40',
        '105.43.53.195':'B29XZwy24VSflXTWPpdhGm2FoTmHfv0JMTLV0Bm043d8c432'
    }

    # Get the current IP address
    ip = get_ip()
    if not ip:
        return "Failed to retrieve IP address."

    print("Your IP address is:", ip)

    # Get the token based on the IP
    token = ip_token_map.get(ip)
    if not token:
        return "Token not found for this IP address."
    url = f'https://www.ivasms.com/api/sms?to={number}'

    # Define headers
    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Send request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        message = response.json()['message']

        # Use regex to extract the code
        match = re.search(r'\d+', message)
        if match:
            code = match.group()
            return code
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
def get_panel_code_api13(number):
    s = requests.Session()
    headers = {
        'Host': 'basha.cc',
        'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i',
        'Connection': 'keep-alive',
    }

    response = s.get('https://basha.cc/login', headers=headers)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the meta tag with the name "csrf-token"
    csrf = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')

    headers = {
        'Host': 'basha.cc',
        # 'Content-Length': '123',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://basha.cc',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://basha.cc/login',
        'Priority': 'u=0, i',
    }

    data = {
        '_token': csrf,
        'email': 'abdomostafa230000@gmail.com',
        'password': 'abdo1746',
        'g-recaptcha-response': '',
    }

    response = s.post('https://basha.cc/login', headers=headers, data=data)

    headers = {
        'Host': 'basha.cc',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://basha.cc/my/messages',
        'Priority': 'u=1, i',
    }

    params = {
        'draw': '2',
        'columns[0][data]': 'country_iso_name',
        'columns[1][data]': 'destination_number',
        'columns[2][data]': 'source_number',
        'columns[3][data]': 'message_text',
        'columns[4][data]': 'message_count',
        'columns[5][data]': 'client_revenue',
        'columns[6][data]': 'timeStamp',
        'order[0][column]': '1',
        'order[0][dir]': 'desc',
        'start': '0',
        'length': '10',
        'search[value]': str(number),
        '_': '1737063902157',
    }

    response = s.get('https://basha.cc/my/messages', params=params, headers=headers)
    data = response.json()
    if data['data']:
        last_message = data['data'][0]['message_text']
        match = re.search(r"\b\d{5,6}\b", last_message)
        if match:
            return match.group()
    return None
def get_panel_code_api14(number,phpsessid):
    cookies = {
        'PHPSESSID': phpsessid,
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=8s9d63nuhk8njc4vm60gmeejei',
        'Referer': 'http://185.2.83.39/ints/agent/SMSCDRStats',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(
        f'http://185.2.83.39/ints/agent/res/data_smscdr.php?fdate1=2024-12-23%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1735036492347',
        cookies=cookies,
        headers=headers,
        timeout=30
    )

    try:
        data = json.loads(response.text)
        # Extract the message
        message_text = data['aaData'][0][5]
        # Search for the verification code
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
def get_panel_code_api15(number):
    def get_ip():
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print("Failed to fetch IP address:", e)
            return None

    # Map of IP addresses to tokens
    ip_token_map = {
        '44.226.145.213': 'HyawVk9yQxaax681QglwdQ',
        '54.187.200.255': 'M04xgNokTeGHLZVaJPpacQ',
        '34.213.214.55': 'vn0ENuJiRtiWZGeJn0ylbg',
        '35.164.95.156': 'V2Uh6p7sTkGY3hslVUvoEg',
        '44.230.95.183': 'y9a8WlyLQSun_tlaQU3REw',
        '44.229.200.200': 'v3niIZ8lQrWelZ62ElQgSg',
    }

    # Get the current IP address
    ip = get_ip()
    if not ip:
        return "Failed to retrieve IP address."

    print("Your IP address is:", ip)

    # Get the token based on the IP
    token = ip_token_map.get(ip)
    if not token:
        return "Token not found for this IP address."
    now = datetime.now(timezone.utc)
    start_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    end_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    headers = {
        'Content-Type': 'application/json',
        'Api-Key': str(token),
    }

    json_data = {
        'id': None,
        'jsonrpc': '2.0',
        'method': 'sms.mdr_full:get_list',
        'params': {
            'filter': {
                'start_date': start_day,
                'end_date': end_day,
                'senderid': '',
                'phone': str(number),
            },
            'page': 1,
            'per_page': 15,
        },
    }

    response = requests.post('https://api.premiumy.net/v1.0', headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json()
        mdr_full_list = data['result']['mdr_full_list']
        if mdr_full_list:  # Check if the list is not empty
            message_text = mdr_full_list[0]['message']
            verification_code = re.search(r"\b\d{5,6}\b", message_text)
            if verification_code:
                return verification_code.group()
            else:
                return None
        else:
            return None
    else:
        return None
    
def get_panel_code_api16(number):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://textnvoice.com/agent/SMSCDRStats',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response1 = requests.get('https://textnvoice.com/login', headers=headers)
    soup = BeautifulSoup(response1.text, 'html.parser')

    # Locate the <label> tag for the captcha
    label_text = soup.find('label', {'for': 'captcha'}).text
    numbers = re.findall(r'\d+', label_text)
    result = int(numbers[0]) + int(numbers[1])
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://textnvoice.com',
        'Referer': 'https://textnvoice.com/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'username': 'abdo1746',
        'password': 'abdo174612',
        'capt': str(result),
    }

    response = requests.post('https://textnvoice.com/signin', cookies=cookies, headers=headers, data=data)



    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://textnvoice.com/agent/SMSCDRStats',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(
        f'https://textnvoice.com/agent/res/data_smscdr.php?fdate1=2025-01-19%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1737320874710',
        cookies=cookies,
        headers=headers,
    )
    try:
        data = json.loads(response.text)
        # Extract the message
        message_text = data['aaData'][0][5]
        # Search for the verification code
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
def get_panel_code_api17(number):
    import requests
    s = requests.Session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://iprndata.callstats.online/sms-stats/overview',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = s.get('https://iprndata.callstats.online/user-management/auth/login', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the input element by its name attribute
    csrf_value = soup.find('input', {'name': '_csrf-frontend'})['value']


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://iprndata.callstats.online',
        'priority': 'u=0, i',
        'referer': 'https://iprndata.callstats.online/user-management/auth/login',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        '_csrf-frontend': csrf_value,
        'LoginForm[username]': 'Abdo123',
        'LoginForm[password]': '321123',
        'LoginForm[identityhash]': '9b48f1ff8d128095f8b0c2eab1d12e5d',
        'LoginForm[rememberMe]': '0',
    }

    response = s.post(
        'https://iprndata.callstats.online/user-management/auth/login',
        headers=headers,
        data=data,
    )
    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cflb=02DiuG31jTeXAcCvB3iGyxR9pDUnHDGkWsdY5ZmXyWXJk; advanced-frontend=jvgvs3sbscsfqjjqhbo652j0jt; _csrf-frontend=4e2e5a4ef062a46dc2b16ca7c7c2e713c3d67b2cc6b5c7e2953b3046f15a94a6a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22sCxJowRnD_dCtkAuNkxbhgNOjJHbJTAJ%22%3B%7D',
        'priority': 'u=1, i',
        'referer': 'https://iprndata.callstats.online/sms-records/index?PartitionSmsInboundAllocationSearch%5Bdate_range%5D=2025-01-25+00%3A00%3A00+-+2025-01-25+23%3A59%3A59&PartitionSmsInboundAllocationSearch%5Bpartition_crm_id_client%5D=',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-csrf-token': 'rO0eqs-1VmfUiNi7usFMP1o0DHXnqogq4FtLKsRFZ4DfrmbgoMIECZDXvPjOqg1KFF90F4_NxmWKEQNIjhEmyg==',
        'x-pjax': 'true',
        'x-pjax-container': '#cdrs-pjax-pjax',
        'x-requested-with': 'XMLHttpRequest',
    }
    current_date = datetime.now().strftime('%Y-%m-%d')
    params = {
        'per-page': '50',
        'PartitionSmsInboundAllocationSearch[partition_crm_id]': '',
        'PartitionSmsInboundAllocationSearch[partition_crm_id_client]': '',
        'PartitionSmsInboundAllocationSearch[source_addr]': '',
        'PartitionSmsInboundAllocationSearch[destination_addr]': str(number),
        'PartitionSmsInboundAllocationSearch[smpp_status]': '',
        'PartitionSmsInboundAllocationSearch[short_message]': '',
        'PartitionSmsInboundAllocationSearch[date_range]': f'2025-01-25 00:00:00 - {current_date} 23:59:59',
        '_pjax': '#cdrs-pjax-pjax',
    }

    response = s.get('https://iprndata.callstats.online/sms-records/index', params=params, headers=headers)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        message_text = soup.find('td', class_='truncate cdrs-pjax').get_text(strip=True)
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
def get_panel_code_api18(number):
    s = requests.Session()
    # Ensure the number does not start with a '+' sign
    if number.startswith('+'):
        number = number[1:]  # Remove the '+' sign
    else:
        number = number  # Keep it as is
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'PHPSESSID=rj4gtfjlcn053k48m31ul6msmc222s4c38fudukadf4q86cp2e50',
        'origin': 'https://mediateluk.com',
        'priority': 'u=0, i',
        'referer': 'https://mediateluk.com/sms/index.php?opt=shw_sts_fin',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"131.0.6778.267"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.267", "Chromium";v="131.0.6778.267", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    params = {
        'login': '1',
    }

    data = {
        'user': '1926',
        'password': 'abdo1024',
    }

    response = s.post('https://mediateluk.com/sms/index.php', params=params, headers=headers, data=data)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://mediateluk.com',
        'priority': 'u=0, i',
        'referer': 'https://mediateluk.com/sms/index.php?opt=shw_sts_today',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"131.0.6778.267"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.267", "Chromium";v="131.0.6778.267", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    params = {
        'opt': 'shw_sts_today_det',
    }

    data = {
        'ddi': f'+{number}',
        'oad': 'Telegram',
    }

    response = s.post('https://mediateluk.com/sms/index.php', params=params, headers=headers, data=data)
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <tr> with class 'table_line_even'
    try:
        message_text = soup.find('tr', class_='table_line_even').find_all('td')[-1].get_text(strip=True)
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None
def get_panel_code_api19(number):
    s = requests.Session()
    # Ensure the number does not start with a '+' sign
    if number.startswith('+'):
        number = number[1:]  # Remove the '+' sign
    else:
        number = number  # Keep it as is
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'advanced-frontend=ntmb2edb8manok55ul7cui67d8',
        'priority': 'u=0, i',
        'referer': 'https://smsportal.live/dashboard',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    response = s.get('https://smsportal.live/user-management/auth/login', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the input element by its name attribute
    csrf_value = soup.find('input', {'name': '_csrf-frontend'})['value']
    cookies = {
        '_csrf-frontend': csrf_value,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'advanced-frontend=splg0q84rsbo5mhj22k8rjsr7m; _csrf-frontend=9688879fa671dd457c9084d3e116915a12fffb89c3d5931115b988cb6a695d2ca%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22qiFqWipr_XGtMaQFpv342jE0MvEkP6Oj%22%3B%7D',
        'origin': 'https://smsportal.live',
        'priority': 'u=0, i',
        'referer': 'https://smsportal.live/user-management/auth/login',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    data = {
        '_csrf-frontend': csrf_value,
        'LoginForm[username]': 'Abdo17461746',
        'LoginForm[password]': 'abdo1746',
        'LoginForm[rememberMe]': '0',
    }

    response = s.post('https://smsportal.live/user-management/auth/login', cookies=cookies, headers=headers, data=data)
    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'advanced-frontend=lodklpvlafruu15f6fs66hr2jd; _csrf-frontend=30007d217a6a3b2e4fc1bd9f75f2977e0ddb89143aa40d37b0ff67fe9e116a68a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22QUFMz7W6Ub49oajqpWKV96ZU-elP6K8r%22%3B%7D',
        'priority': 'u=1, i',
        'referer': 'https://smsportal.live/sms-records/index?PartitionSmsInboundAllocationSearch%5Bdate_range%5D=2025-02-04+00%3A00%3A00+-+2025-02-04+23%3A59%3A59&PartitionSmsInboundAllocationSearch%5Bpartition_crm_id_client%5D=',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-csrf-token': 'IJVFMYDtZ_IJnMryOiDMxx0hacwOeh_9vQbD9_qowWNxwAN8-towxFz-_stVQaa2bXYimjdMRaiQY6-nzOP5EQ==',
        'x-pjax': 'true',
        'x-pjax-container': '#cdrs-pjax-pjax',
        'x-requested-with': 'XMLHttpRequest',
    }

    current_date = datetime.now().strftime('%Y-%m-%d')
    params = {
        'per-page': '50',
        'PartitionSmsInboundAllocationSearch[partition_crm_id]': '',
        'PartitionSmsInboundAllocationSearch[partition_crm_id_client]': '',
        'PartitionSmsInboundAllocationSearch[source_addr]': '',
        'PartitionSmsInboundAllocationSearch[destination_addr]': str(number),
        'PartitionSmsInboundAllocationSearch[smpp_status]': '',
        'PartitionSmsInboundAllocationSearch[short_message]': '',
        'PartitionSmsInboundAllocationSearch[date_range]': f'2025-01-25 00:00:00 - {current_date} 23:59:59',
        '_pjax': '#cdrs-pjax-pjax',
    }

    response = s.get('https://smsportal.live/sms-records/index', params=params, cookies=cookies, headers=headers)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        message_text = soup.find('td', class_='truncate cdrs-pjax').get_text(strip=True)
        verification_code = re.search(r"\b\d{5,6}\b", message_text)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None


def get_panel_code_api20(number):
    cookies = {
        'PHPSESSID': '37ola9lb381auj5q4dn929cegt',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'http://85.195.94.50/sms/client/Reports',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    current_date = datetime.now().strftime('%Y-%m-%d')
    try:
        response = requests.get(
            f'http://85.195.94.50/sms/client/ajax/dt_reports.php?fdate1=2025-02-13%2000:00:00&fdate2={current_date}%2023:59:59&ftermination=&fclient=&fnum={number}&fcli=Telegram&fgdate=0&fgtermination=0&fgclient=0&fgnumber=0&fgcli=0&fg=0&sEcho=1&iColumns=11&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=true&mDataProp_9=9&sSearch_9=&bRegex_9=false&bSearchable_9=true&bSortable_9=true&mDataProp_10=10&sSearch_10=&bRegex_10=false&bSearchable_10=true&bSortable_10=true&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1739462959859',
            cookies=cookies,
            headers=headers,
        )

        data = response.json()['aaData'][0][10]
        verification_code = re.search(r"\b\d{5,6}\b", data)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api21(number):
    s = requests.Session()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'PHPSESSID=mjngtganc4iolchngqrg0h0pp2',
    }

    response = s.get('https://panel.iprn-sms.com/login', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf_token'})['value']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://panel.iprn-sms.com',
        'Referer': 'https://panel.iprn-sms.com/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        '_csrf_token': csrf_token,
        '_username': 'abdo1746',
        '_password': 'asudTR56',
        '_submit': 'Login',
    }

    response = s.post('https://panel.iprn-sms.com/login_check', headers=headers, data=data)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://panel.iprn-sms.com/premium_number/stats/sms',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    current_date = datetime.now().strftime("%d/%m/%Y")
    try:
        response = s.get(
            f'https://panel.iprn-sms.com/api/helper/premium-number/stats/sms.json?date_from={current_date}%2000&date_to={current_date}%2023&currency_id=1&draw=9&columns%5B0%5D%5Bdata%5D=source&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=name&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=short_code&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=%5E{number}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=true&columns%5B3%5D%5Bdata%5D=phone_number&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=payout&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=message&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=notified&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=created&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=25&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1741102261390',
            headers=headers,
        )
        message = json.loads(response.text)['aaData'][0]['message']
        verification_code = re.search(r'\d+', message)
        if verification_code:
            return verification_code.group()
        else:
            return None
    except:
        return None

def get_panel_code_api22(number):
    """
    Check if a voice file exists for the given number ID
    Args:
        number: The ID of the voice file to check
    Returns:
        str: The URL if the file exists, "Failed" if it doesn't
    """
    try:
        url = f'https://panelsms.onrender.com/play/{number}'
        response = requests.get(url)
        if response.status_code == 200:
            return url
        return "Failed"
    except Exception as e:
        return "Failed"

def get_verification_code3(number, user, password):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'http://51.178.79.51/NumberPanel/agent/SMSDashboard',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response1 = requests.get('http://51.178.79.51/NumberPanel/login', headers=headers)
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
        # 'Cookie': 'PHPSESSID=ag67srbm45h1f0b2vf7u58t0qb',
        'Origin': 'http://51.178.79.51',
        'Referer': 'http://51.178.79.51/NumberPanel/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'username': user,
        'password': password,
        'capt': str(result),
    }

    response = requests.post('http://51.178.79.51/NumberPanel/signin', cookies=cookies, headers=headers, data=data, verify=False)
    cookies = {
        'PHPSESSID': response1.cookies['PHPSESSID'],
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=kvbs85l6e2ne81feafqngih2ff',
        'Referer': 'http://51.178.79.51/NumberPanel/agent/SMSCDRReports',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # Get the current date in the required format (YYYY-MM-DD HH:MM:SS)
    current_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(f'http://51.178.79.51/NumberPanel/agent/res/data_smscdr.php?fdate1=2024-12-08%2000:00:00&fdate2={current_date}%2023:59:59&frange=&fclient=&fnum={number}&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1733682941115',
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

def get_verification_code4(number,user,password):

    api_url = 'http://zivastats.com/rest/sms'

    auth_hash = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")

    # Set the headers including the Authorization header
    headers = {
        "Authorization": f"Basic {auth_hash}"
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
                code = re.search(r'\d+', short_message)
                if code:
                    return code.group()  # Return the extracted code
    
    # If the destination_addr wasn't found or there was an error
    return None