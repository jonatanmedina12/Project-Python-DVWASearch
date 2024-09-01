import time
from censys.common.exceptions import CensysException
from dotenv import load_dotenv
import os
from src.censys_controller.censys_search import CensysController
from src.censys_controller.login_automation_censys import verify_dvwa, attempt_login
from src.shodan_controller.shodan_search import ShodanSearch

load_dotenv()


def shodan_exec():
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

    if not SHODAN_API_KEY:
        print("Error: No se encontró la clave API de Shodan en las variables de entorno.")
        return

    search_ = ShodanSearch(SHODAN_API_KEY)
    quota=search_.check_shodan_api()
    if not quota:
        print("No se pudo obtener información de la cuota. Abortando la búsqueda.")
        return

    if quota['allowance'] - quota['used'] <= 0:
        print("Has alcanzado tu límite de búsquedas. Por favor, espera hasta el próximo ciclo.")
        return

    resultado = search_.search("title:dvwa", page=1)

    if resultado is None:
        print("No se pudieron obtener resultados.")
        return

    print(f"Total de resultados encontrados: {resultado.get('total', 0)}")

    for i, match in enumerate(resultado.get('matches', [])[:10]):
        print(f"\nResultado {i + 1}")
        print(f"Dirección IP: {match.get('ip_str', 'N/A')}")
        print(f"Hostname: {', '.join(match.get('hostnames', ['N/A']))}")
        print(f"Localización: {match.get('location', {}).get('country_name', 'N/A')}, "
              f"{match.get('location', {}).get('city', 'N/A')}")

def censys_exec():
    API_ID = os.getenv("CENSYS_API_ID")
    API_SECRET = os.getenv("CENSYS_API_SECRET")


    if not API_ID or not API_SECRET:
        print("Error: No se encontraron las credenciales de Censys en las variables de entorno.")
        return

    try:
        h = CensysController(api_id=API_ID, api_secret=API_SECRET)
        quota = h.check_censys_quota()
        if not quota:
            print("No se pudo obtener información de la cuota. Abortando la búsqueda.")
            return

        if quota['allowance'] - quota['used'] <= 0:
            print("Has alcanzado tu límite de búsquedas. Por favor, espera hasta el próximo ciclo.")
            return
        # Consulta para buscar posibles instancias de DVWA
        query = '(services.http.response.html_title: "Damn Vulnerable Web Application") OR (services.http.response.body: "DVWA")'
        results = h.search(query,page=1, per_page=2)
        total_results = 0
        for page in results:
            print(page)
            for result in page:
                ip = result.get('ip', 'N/A')
                print(f"\nComprobando IP: {ip}")

                services = result.get('services', [])
                for service in services:
                    if service.get('service_name') in ['HTTP', 'HTTPS']:
                        port = service.get('port', 80)
                        protocol = 'https' if service.get('service_name') == 'HTTPS' else 'http'
                        url = f"{protocol}://{ip}:{port}/login.php"

                        print(f"Verificando DVWA en {url}")
                        if verify_dvwa(url):
                            print(f"[+] DVWA encontrado en {url}")
                            if attempt_login(url):
                                print(f"[+] Login exitoso en {url}")
                            else:
                                print(f"[-] Login fallido en {url}")
                        else:
                            print(f"[-] No se encontró DVWA en {url}")

                        time.sleep(2)
        print("---")

        print(f"\nTotal de posibles instancias DVWA encontradas: {total_results}")

    except CensysException as e:
        print(f"Error en la API de Censys: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")