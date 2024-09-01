import re

import requests


def verify_dvwa(url):
    try:
        response = requests.get(url, verify=False, timeout=10)
        return "Damn Vulnerable Web Application" in response.text
    except requests.RequestException:
        return False

def attempt_login(url):
    session = requests.Session()
    try:
        response = session.get(url, verify=False, timeout=10)
        if response.status_code != 200:
            return False

        token_match = re.search(r"user_token' value='([0-9a-f]+)'", response.text)
        if not token_match:
            return False

        token = token_match.group(1)
        login_data = {
            "username": "admin",
            "password": "password",
            "user_token": token,
            "Login": "Login"
        }

        response = session.post(
            url,
            data=login_data,
            allow_redirects=False,
            verify=False,
            timeout=10,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        return response.status_code == 302 and response.headers.get('location') == 'index.php'
    except requests.RequestException:
        return False
