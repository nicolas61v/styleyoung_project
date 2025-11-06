"""
Interfaz para generación de reportes - Inversión de Dependencias (SOLID)

Este módulo implementa el patrón de Inversión de Dependencias (Dependency Inversion Principle)
mediante una interfaz abstracta y múltiples implementaciones concretas.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from django.http import HttpResponse


class ReporteInterface(ABC):
    """
    Interfaz abstracta para generación de reportes

    Esta interfaz define el contrato que deben cumplir todas las implementaciones
    de generadores de reportes. Permite agregar nuevos formatos de reporte sin
    modificar el código existente (Open/Closed Principle).
    """

    @abstractmethod
    def generar_reporte(self, titulo: str, datos: List[Dict[str, Any]], columnas: List[str]) -> HttpResponse:
        """
        Genera un reporte con los datos proporcionados

        Args:
            titulo: Título del reporte
            datos: Lista de diccionarios con los datos a incluir
            columnas: Lista de nombres de columnas a mostrar

        Returns:
            HttpResponse con el archivo del reporte
        """
        pass

    @abstractmethod
    def get_content_type(self) -> str:
        """Retorna el content type del formato de reporte"""
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """Retorna la extensión del archivo de reporte"""
        pass
