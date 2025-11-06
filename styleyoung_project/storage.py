"""
Configuración personalizada de almacenamiento para S3
"""
import os
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Storage personalizado para archivos de media en S3
    Almacena los archivos en la carpeta 'media' del bucket
    """
    location = os.getenv('AWS_LOCATION', 'media')
    file_overwrite = False  # No sobrescribir archivos si ya existen
    default_acl = os.getenv('AWS_DEFAULT_ACL', 'public-read')
