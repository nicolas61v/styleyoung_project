"""
Template tags para breadcrumbs navigation
"""
from django import template

register = template.Library()


@register.inclusion_tag('snippets/breadcrumbs.html')
def breadcrumbs(items):
    """
    Renderiza un componente de breadcrumbs

    Args:
        items: Lista de diccionarios con 'name' y 'url' (url opcional para el último item)

    Ejemplo de uso:
        {% load breadcrumb_tags %}
        {% breadcrumbs breadcrumb_items %}

    Donde breadcrumb_items en el contexto es:
        [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Productos', 'url': '/productos/'},
            {'name': 'Nombre del Producto'}
        ]
    """
    return {'items': items}
