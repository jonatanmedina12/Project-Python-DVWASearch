import re

import requests


def has_valid_credentials(instance):
    session = requests.Session()
    proto = 'https' if 'ssl' in instance else 'http'
    login_page = f"{proto}://{instance['ip_str']}:{instance['port']}/login.php"
    try:
        response = session.get(login_page,verify=False)

    except requests.exceptions.ConnectionError as e:
        print(f"Error al conectarse al host {instance['ip_str']}: {e}")
        return False

    if response.status_code !=200:
        print(f"[!] Error en la respuesta del servidor : {response.status_code}")
        return  False

    # obtener el token CSRF

    token = re.search(r"user_token' value='([0-9a-f]+)'",response.text).group(1)

    response = session.post(
        login_page,
        f"username=admin&password=password&user_token={token}&Login=Login",
        allow_redirects=False,
        verify=False,
        headers={'content-Type':'application/x-ww-form-urlencoded'}
    )
    # si la respuesta es un direccion al index esta bien
    if response.status_code == 302 and response.headers['location'] == 'index.php':
        return True
    else:
        return  False

