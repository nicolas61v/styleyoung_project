from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import Producto, Categoria, ImagenProducto, Talla


class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos con imagen"""
    
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'marca', 
            'color', 'material', 'categoria', 'imagen_principal'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'material': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Material'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'imagen_principal': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'marca': 'Marca',
            'color': 'Color',
            'material': 'Material',
            'categoria': 'Categoría',
            'imagen_principal': 'Imagen Principal'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar categorías disponibles
        self.fields['categoria'].queryset = Categoria.objects.all()


class ImagenProductoForm(forms.ModelForm):
    """Formulario para añadir imágenes adicionales a productos"""
    
    class Meta:
        model = ImagenProducto
        fields = ['imagen', 'descripcion', 'es_principal', 'orden']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la imagen (opcional)'
            }),
            'es_principal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            })
        }
        labels = {
            'imagen': 'Imagen',
            'descripcion': 'Descripción',
            'es_principal': 'Marcar como imagen principal',
            'orden': 'Orden de visualización'
        }


class TallaForm(forms.ModelForm):
    """Formulario para crear/editar tallas de productos"""

    class Meta:
        model = Talla
        fields = ['talla', 'stock']
        widgets = {
            'talla': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'min': '0',
                'value': '0'
            })
        }
        labels = {
            'talla': 'Talla',
            'stock': 'Cantidad/Stock'
        }


# FormSet para manejar múltiples tallas en un producto
TallaFormSet = modelformset_factory(
    Talla,
    form=TallaForm,
    extra=5,  # Mostrar 5 filas vacías por defecto
    can_delete=True,
    min_num=0,
    validate_min=False
)


class CategoriaForm(forms.ModelForm):
    """Formulario para crear/editar categorías"""

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            })
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción'
        }