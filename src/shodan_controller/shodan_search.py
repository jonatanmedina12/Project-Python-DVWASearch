import pkg_resources
import shodan


class ShodanSearch:
    def __init__(self, api_key):
        self.shoda_Api_key =api_key
        self.client = shodan.Shodan(api_key)

    def search(self, query, page=1):
        try:
            results = self.client.search(query, page=page)
            return results
        except shodan.APIError as e:
            print(f"Error en la API de Shodan: {e}")
            return None

    def check_shodan_api(self):
        if not self.shoda_Api_key:
            print("Error: No se encontró la clave API de Shodan en las variables de entorno.")
            return

        print(f"Clave API cargada: {self.shoda_Api_key[:5]}...{self.shoda_Api_key[-5:]}")
        print(f"Longitud de la clave API: {len(self.shoda_Api_key)}")

        try:
            # Obtener la versión de Shodan
            shodan_version = pkg_resources.get_distribution("shodan").version
            print(f"Versión de la biblioteca Shodan: {shodan_version}")

            api = shodan.Shodan(self.shoda_Api_key)

            # Intenta obtener información de la cuenta
            account_info = api.info()
            print("\nInformación de la cuenta:")
            print(f"Plan: {account_info.get('plan')}")
            print(f"Consultas restantes: {account_info.get('query_credits')}")

            if account_info.get('query_credits', 0) > 0:
                # Intenta una búsqueda simple solo si hay créditos disponibles
                results = api.search('apache', limit=1)
                print(f"\nResultados de búsqueda para 'apache': {results.get('total', 0)}")
            else:
                print("\nNo hay créditos de consulta disponibles. No se realizará la búsqueda.")

        except shodan.APIError as e:
            print(f"Error en la API de Shodan: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
