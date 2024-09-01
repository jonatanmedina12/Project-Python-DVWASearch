# Proyecto de Búsqueda y Verificación de DVWA

## Descripción
Este proyecto utiliza la API de Censys y Shodan para buscar potenciales instancias de Damn Vulnerable Web Application (DVWA) en Internet. Luego, verifica cada instancia encontrada e intenta realizar un login automático utilizando credenciales por defecto.

### Advertencia
Este script está diseñado únicamente con fines educativos y de investigación. El uso de este script para acceder a sistemas sin autorización expresa puede ser ilegal. Asegúrate de tener permiso antes de escanear o intentar acceder a cualquier sistema que no sea de tu propiedad.

## Requisitos

- Python 3.6+
- Cuenta de Censys (gratuita o de pago)
- Cuenta de Shodan (gratuita o de pago)
- Bibliotecas de Python: `censys`, `requests`, `python-dotenv`,`shodan`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/jonatanmedina12/Python-Project-DVWA-Search.git
    cd Python-Project-DVWA-Search
    ```

2. Instala las dependencias:
    ```bash
    pip install censys requests python-dotenv
    ```

3. Configura tus credenciales de Censys:
    Crea un archivo `.env` en el directorio raíz del proyecto y añade tus credenciales de Censys:
    ```bash
    SHODAN_API_KEY=tu_api_Key
    CENSYS_API_ID=tu_api_id
    CENSYS_API_SECRET=tu_api_secret
    ```

## Uso

Ejecuta el script principal:
```bash
python main.py
```
## Licencia
Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.
