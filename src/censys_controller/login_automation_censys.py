import re
import time

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

def process_result(result):
    # Verificamos si el resultado es una lista y tomamos el primer elemento si es así
    if isinstance(result, list) and result:
        result = result[0]

    # Ahora verificamos si el resultado es un diccionario
    if not isinstance(result, dict):
        print(f"Resultado inesperado: {result}")
        return False

    ip = result.get('ip', 'N/A')
    print(f"\nComprobando IP: {ip}")
    found_dvwa = False
    contador =0
    services = result.get('services', [])
    for service in services:
        if isinstance(service, dict) and service.get('service_name') in ['HTTP', 'HTTPS']:
            contador += 1
            port = service.get('port', 80)
            protocol = 'https' if service.get('service_name') == 'HTTPS' else 'http'
            url = f"{protocol}://{ip}:{port}/login.php"
            print(f"------------------------PETICIÓN {contador} --------------------------")
            print(f"Verificando DVWA en {url}")
            if verify_dvwa(url):
                print(f"[+] DVWA encontrado en {url}")
                if attempt_login(url):
                    print(f"[+] Login exitoso en {url}")
                else:
                    print(f"[-] Login fallido en {url}")
                found_dvwa = True
            else:
                print(f"[-] No se encontró DVWA en {url}")

            print(f"------------------------FINAL PETICIÓN {contador} ------------------- \n")
            time.sleep(2)

    return found_dvwa