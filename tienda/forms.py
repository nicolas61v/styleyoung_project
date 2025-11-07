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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos opcionales para permitir filas vacías en el formset
        self.fields['talla'].required = False
        self.fields['stock'].required = False

    def clean(self):
        """Validación personalizada: si hay datos en una fila, ambos campos deben estar completos"""
        cleaned_data = super().clean()
        talla = cleaned_data.get('talla')
        stock = cleaned_data.get('stock')

        # Si está marcado para eliminar, no validar
        if self.cleaned_data.get('DELETE'):
            return cleaned_data

        # Si hay talla pero no stock, o viceversa
        if (talla and not stock is not None) or (stock is not None and not talla):
            # Si ambos están vacíos, está bien (fila vacía)
            if talla or stock is not None:
                raise forms.ValidationError(
                    "Si especificas una talla, debes incluir el stock también."
                )

        return cleaned_data


# FormSet para manejar múltiples tallas en un producto
TallaFormSet = modelformset_factory(
    Talla,
    form=TallaForm,
    extra=5,  # Mostrar 5 filas vacías por defecto
    can_delete=True,
    min_num=0,  # Permitir 0 en el formset, la validación está en la vista
    validate_min=False  # No validar aquí, validamos en la vista
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