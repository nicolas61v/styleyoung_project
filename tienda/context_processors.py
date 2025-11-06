"""
Context processors personalizados para la aplicación tienda

Los context processors agregan variables al contexto de todas las plantillas automáticamente
"""
from .services.clima_service import ClimaService


def clima_context(request):
    """
    Agrega información del clima al contexto de todas las plantillas

    Returns:
        dict: Diccionario con información del clima
    """
    clima = ClimaService.obtener_clima()

    return {
        'clima_actual': clima
    }
