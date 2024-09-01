from censys.search import CensysHosts
from censys.common.exceptions import CensysException

class CensysController:
    def __init__(self, api_id, api_secret):
        self.api_id_=api_id
        self.secret_data = api_secret
        self.client = CensysHosts(api_id=api_id, api_secret=api_secret)

    def search(self, query, page=1, per_page=2, fields=None):
        try:
            results = self.client.search(
                query,
                page=page,
                per_page=per_page,
                fields=fields
            )
            return results
        except CensysException as e:
            print(f"Error en la API de Censys: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def get_host_details(self, ip):
        try:
            host = self.client.view(ip)
            return host
        except CensysException as e:
            print(f"Error al obtener detalles del host: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def check_censys_quota(self):

        if not  self.api_id_ or not  self.secret_data :
            print("Error: No se encontraron las credenciales de Censys en las variables de entorno.")
            return

        try:
            h = CensysHosts(api_id=self.api_id_, api_secret=self.secret_data)
            quota = h.quota()

            print("Información de cuota de Censys:")
            print(f"Búsquedas utilizadas este mes: {quota['used']}")
            print(f"Límite mensual de búsquedas: {quota['allowance']}")
            print(f"Búsquedas restantes: {quota['allowance'] - quota['used']}")

            # Verificar si estamos cerca del límite
            if quota['used'] >= quota['allowance'] * 0.9:  # 90% del límite
                print("¡Advertencia! Estás cerca de alcanzar tu límite mensual de búsquedas.")

            return quota

        except CensysException as e:
            print(f"Error al consultar la cuota de Censys: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        return None