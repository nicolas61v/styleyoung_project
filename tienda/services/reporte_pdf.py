"""
Implementación concreta de ReporteInterface para generar reportes en PDF
"""
from typing import List, Dict, Any
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from .reporte_interface import ReporteInterface


class ReportePDF(ReporteInterface):
    """
    Generador de reportes en formato PDF

    Implementación concreta que genera reportes utilizando ReportLab.
    Esta clase puede ser utilizada sin modificar el código cliente gracias
    a la inversión de dependencias.
    """

    def generar_reporte(self, titulo: str, datos: List[Dict[str, Any]], columnas: List[str]) -> HttpResponse:
        """
        Genera un reporte en formato PDF

        Args:
            titulo: Título del reporte
            datos: Lista de diccionarios con los datos
            columnas: Lista de columnas a incluir en el reporte

        Returns:
            HttpResponse con el PDF generado
        """
        # Crear buffer en memoria
        buffer = BytesIO()

        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        titulo_style = styles['Heading1']
        elements.append(Paragraph(titulo, titulo_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Fecha de generación
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        fecha_style = styles['Normal']
        elements.append(Paragraph(f"Fecha de generación: {fecha_actual}", fecha_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Preparar datos para la tabla
        tabla_datos = []

        # Encabezados
        tabla_datos.append(columnas)

        # Filas de datos
        for item in datos:
            fila = []
            for columna in columnas:
                valor = item.get(columna, '')
                # Formatear valores según tipo
                if isinstance(valor, (int, float)):
                    if 'precio' in columna.lower() or 'total' in columna.lower():
                        valor = f"${valor:,.2f}"
                    else:
                        valor = str(valor)
                else:
                    valor = str(valor)
                fila.append(valor)
            tabla_datos.append(fila)

        # Crear tabla
        tabla = Table(tabla_datos)

        # Estilo de la tabla
        tabla.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Datos
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            # Alternar colores en filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))

        elements.append(tabla)

        # Pie de página
        elements.append(Spacer(1, 0.5 * inch))
        pie_style = styles['Normal']
        elements.append(Paragraph("StyleYoung - Tienda Virtual de Ropa", pie_style))
        elements.append(Paragraph(f"Total de registros: {len(datos)}", pie_style))

        # Construir PDF
        doc.build(elements)

        # Obtener contenido del buffer
        pdf_content = buffer.getvalue()
        buffer.close()

        # Crear respuesta HTTP
        response = HttpResponse(pdf_content, content_type=self.get_content_type())
        response['Content-Disposition'] = f'attachment; filename="reporte_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{self.get_extension()}"'

        return response

    def get_content_type(self) -> str:
        """Retorna el content type para PDF"""
        return 'application/pdf'

    def get_extension(self) -> str:
        """Retorna la extensión de archivo para PDF"""
        return 'pdf'
