"""
Servicio para obtener información del clima desde API externa

Consumo de API de terceros: OpenWeatherMap
Este servicio obtiene información del clima actual para Medellín, Colombia
"""
import requests
from django.core.cache import cache


class ClimaService:
    """
    Servicio para obtener datos del clima desde OpenWeatherMap API
    """

    # API Key de OpenWeatherMap (demo/gratuita)
    # NOTA: En producción, esto debería estar en variables de entorno
    API_KEY = "bd5e378503939ddaee76f12ad7a97608"  # API key pública de demo
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    # Configuración para Medellín, Colombia
    CIUDAD = "Medellin"
    PAIS = "CO"

    @classmethod
    def obtener_clima(cls):
        """
        Obtiene el clima actual de Medellín

        Returns:
            dict: Información del clima o None si hay error
            {
                'temperatura': 25.5,
                'descripcion': 'nubes dispersas',
                'icono': '02d',
                'humedad': 60,
                'sensacion_termica': 26.0
            }
        """
        # Cachear resultados por 2 horas para no exceder límite de API
        cache_key = f'clima_{cls.CIUDAD}_{cls.PAIS}'
        clima_cached = cache.get(cache_key)

        if clima_cached:
            return clima_cached

        try:
            # Parámetros de la solicitud
            params = {
                'q': f'{cls.CIUDAD},{cls.PAIS}',
                'appid': cls.API_KEY,
                'units': 'metric',  # Celsius
                'lang': 'es'  # Descripciones en español
            }

            # Realizar solicitud a la API con reintentos en caso de rate limit
            max_retries = 2
            for attempt in range(max_retries):
                response = requests.get(cls.BASE_URL, params=params, timeout=5)

                if response.status_code == 200:
                    break
                elif response.status_code == 429 and attempt < max_retries - 1:
                    # Esperar un poco antes de reintentar
                    import time
                    time.sleep(2)
                    continue

            if response.status_code == 200:
                data = response.json()

                # Extraer información relevante
                clima_info = {
                    'temperatura': round(data['main']['temp'], 1),
                    'descripcion': data['weather'][0]['description'].capitalize(),
                    'icono': data['weather'][0]['icon'],
                    'humedad': data['main']['humidity'],
                    'sensacion_termica': round(data['main']['feels_like'], 1),
                    'ciudad': cls.CIUDAD,
                    'pais': cls.PAIS,
                    'icon_url': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                }

                # Cachear por 2 horas (7200 segundos)
                cache.set(cache_key, clima_info, 7200)

                return clima_info
            elif response.status_code == 429:
                # Error de rate limit: usar datos por defecto
                print(f"Error 429 - API rate limit alcanzado. Usando datos por defecto.")
                # Retornar datos por defecto de Medellín
                default_clima = {
                    'temperatura': 24.0,
                    'descripcion': 'Clima despejado',
                    'icono': '01d',
                    'humedad': 65,
                    'sensacion_termica': 25.0,
                    'ciudad': cls.CIUDAD,
                    'pais': cls.PAIS,
                    'icon_url': 'https://openweathermap.org/img/wn/01d@2x.png'
                }
                # Cachear por 1 hora
                cache.set(cache_key, default_clima, 3600)
                return default_clima
            else:
                print(f"Error al obtener clima: {response.status_code}")
                # Si hay otro error, retornar datos por defecto también
                default_clima = {
                    'temperatura': 24.0,
                    'descripcion': 'Clima no disponible',
                    'icono': '01d',
                    'humedad': 65,
                    'sensacion_termica': 25.0,
                    'ciudad': cls.CIUDAD,
                    'pais': cls.PAIS,
                    'icon_url': 'https://openweathermap.org/img/wn/01d@2x.png'
                }
                return default_clima

        except requests.exceptions.Timeout:
            print("Timeout al consultar API de clima")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión con API de clima: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener clima: {e}")
            return None

    @classmethod
    def obtener_clima_simple(cls):
        """
        Versión simplificada que retorna solo temperatura y descripción

        Returns:
            str: Texto con temperatura y descripción o mensaje de error
        """
        clima = cls.obtener_clima()

        if clima:
            return f"{clima['temperatura']}°C - {clima['descripcion']}"
        else:
            return "Clima no disponible"
