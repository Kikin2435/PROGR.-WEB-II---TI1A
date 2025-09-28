from django import forms
from django.core.exceptions import ValidationError
from .models import Car, Document, Profile


# 1. FORMULARIO BÁSICO - Como en el ejemplo de la documentación
class NameForm(forms.Form):
    """
    Formulario simple para obtener el nombre del usuario.
    Ejemplo básico de la documentación de Django.
    """
    your_name = forms.CharField(
        label="Tu nombre", 
        max_length=100,
        help_text="Ingresa tu nombre completo"
    )


# 2. FORMULARIO DE CONTACTO - Ejemplo más complejo
class ContactForm(forms.Form):
    """
    Formulario de contacto que demuestra diferentes tipos de campos.
    """
    subject = forms.CharField(
        max_length=100,
        label="Asunto",
        help_text="Describe brevemente el tema"
    )
    message = forms.CharField(
        widget=forms.Textarea,
        label="Mensaje",
        help_text="Escribe tu mensaje detallado"
    )
    sender = forms.EmailField(
        label="Tu email",
        help_text="Usaremos este email para responderte"
    )
    cc_myself = forms.BooleanField(
        required=False,
        label="Enviarme una copia",
        help_text="Marcar para recibir una copia del mensaje"
    )

    def clean_subject(self):
        """
        Validación personalizada para el campo subject
        """
        subject = self.cleaned_data['subject']
        if len(subject) < 5:
            raise ValidationError("El asunto debe tener al menos 5 caracteres")
        return subject


# 3. MODELFORMS - Formularios basados en modelos existentes

class CarForm(forms.ModelForm):
    """
    Formulario para crear/editar vehículos.
    Basado en el modelo Car usando ModelForm.
    """
    class Meta:
        model = Car
        fields = ['name', 'price', 'photo', 'specs']
        labels = {
            'name': 'Nombre del vehículo',
            'price': 'Precio',
            'photo': 'Fotografía',
            'specs': 'Especificaciones',
        }
        help_texts = {
            'name': 'Ingresa el modelo y marca del vehículo',
            'price': 'Precio en dólares',
            'photo': 'Sube una imagen del vehículo (JPG, PNG)',
            'specs': 'Archivo PDF con las especificaciones',
        }
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'specs': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

    def clean_price(self):
        """
        Validación personalizada para el precio
        """
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("El precio debe ser mayor a cero")
        if price > 1000000:
            raise ValidationError("El precio parece demasiado alto")
        return price


class DocumentForm(forms.ModelForm):
    """
    Formulario para subir documentos
    """
    class Meta:
        model = Document
        fields = ['title', 'file']
        labels = {
            'title': 'Título del documento',
            'file': 'Archivo',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ej: Manual de usuario, Contrato, etc.'
            }),
            'file': forms.FileInput(attrs={
                'accept': '.pdf,.doc,.docx,.txt'
            }),
        }


class ProfileForm(forms.ModelForm):
    """
    Formulario para perfil de usuario
    """
    class Meta:
        model = Profile
        fields = ['username', 'avatar', 'resume']
        labels = {
            'username': 'Nombre de usuario',
            'avatar': 'Foto de perfil',
            'resume': 'Currículum vitae',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
            'resume': forms.FileInput(attrs={'accept': '.pdf'}),
        }

    def clean_username(self):
        """
        Validación para nombre de usuario único
        """
        username = self.cleaned_data['username']
        if Profile.objects.filter(username=username).exists():
            if not self.instance.pk or self.instance.username != username:
                raise ValidationError("Este nombre de usuario ya está en uso")
        return username


# 4. FORMULARIO CON VALIDACIONES AVANZADAS

class SearchForm(forms.Form):
    """
    Formulario de búsqueda con diferentes opciones
    """
    SEARCH_CHOICES = [
        ('cars', 'Vehículos'),
        ('documents', 'Documentos'),
        ('profiles', 'Perfiles'),
        ('all', 'Todo'),
    ]
    
    query = forms.CharField(
        max_length=200,
        label="Buscar",
        help_text="Ingresa términos de búsqueda",
        widget=forms.TextInput(attrs={
            'placeholder': 'Escribe aquí tu búsqueda...',
            'class': 'form-control'
        })
    )
    
    search_in = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        label="Buscar en",
        initial='all',
        help_text="Selecciona dónde buscar"
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Precio mínimo",
        help_text="Solo para búsqueda en vehículos",
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Precio máximo",
        help_text="Solo para búsqueda en vehículos",
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

    def clean(self):
        """
        Validación que involucra múltiples campos
        """
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price:
            if min_price >= max_price:
                raise ValidationError(
                    "El precio mínimo debe ser menor al precio máximo"
                )
        
        return cleaned_data


# 5. FORMULARIO CON CAMPOS DINÁMICOS

class DynamicFieldForm(forms.Form):
    """
    Ejemplo de formulario que puede tener campos dinámicos
    """
    def __init__(self, *args, **kwargs):
        # Extraer parámetros personalizados
        show_advanced = kwargs.pop('show_advanced', False)
        super().__init__(*args, **kwargs)
        
        # Campos básicos siempre presentes
        self.fields['basic_field'] = forms.CharField(
            label="Campo básico",
            max_length=100
        )
        
        # Agregar campos avanzados condicionalmente
        if show_advanced:
            self.fields['advanced_field'] = forms.CharField(
                label="Campo avanzado",
                required=False,
                help_text="Este campo solo aparece en modo avanzado"
            )
            self.fields['color_preference'] = forms.ChoiceField(
                choices=[
                    ('red', 'Rojo'),
                    ('blue', 'Azul'),
                    ('green', 'Verde'),
                ],
                label="Color preferido",
                required=False
            )


# ======================================================================
# FILE UPLOADS - Implementación de la documentación Django File Uploads
# ======================================================================

# 1. FORMULARIO BÁSICO DE SUBIDA DE ARCHIVO
class UploadFileForm(forms.Form):
    """
    Formulario básico para subir archivos.
    Ejemplo directo de la documentación Django.
    """
    title = forms.CharField(
        max_length=50,
        label="Título del archivo",
        help_text="Nombre descriptivo para el archivo"
    )
    file = forms.FileField(
        label="Seleccionar archivo",
        help_text="Selecciona un archivo para subir"
    )

    def clean_file(self):
        """
        Validación personalizada para el archivo
        """
        file = self.cleaned_data['file']
        if file:
            # Limitar tamaño a 10MB
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("El archivo no puede ser mayor a 10MB")
            
            # Verificar extensiones permitidas
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.png']
            ext = file.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise ValidationError(
                    f"Extensión no permitida. Permitidas: {', '.join(allowed_extensions)}"
                )
        
        return file


# 2. FORMULARIO CON MODELO (ModelForm)
class ModelFormWithFileField(forms.ModelForm):
    """
    ModelForm que maneja archivos automáticamente.
    El archivo se guarda usando el campo FileField del modelo.
    """
    class Meta:
        model = Document
        fields = ['title', 'file']
        labels = {
            'title': 'Título del documento',
            'file': 'Archivo del documento'
        }
        help_texts = {
            'title': 'Nombre descriptivo del documento',
            'file': 'Selecciona el archivo a subir (se guardará automáticamente)'
        }


# 3. SUBIDA MÚLTIPLE DE ARCHIVOS - Widget personalizado

class MultipleFileInput(forms.ClearableFileInput):
    """
    Widget personalizado que permite seleccionar múltiples archivos.
    Implementación según documentación Django.
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    Campo personalizado que maneja múltiples archivos.
    Extiende FileField para procesar listas de archivos.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    """
    Formulario que usa el campo de múltiples archivos.
    """
    title = forms.CharField(
        max_length=100,
        label="Título del lote",
        help_text="Nombre para identificar este conjunto de archivos"
    )
    file_field = MultipleFileField(
        label="Seleccionar múltiples archivos",
        help_text="Puedes seleccionar varios archivos a la vez (Ctrl+Click)"
    )

    def clean_file_field(self):
        """
        Validación para múltiples archivos
        """
        files = self.cleaned_data['file_field']
        
        if len(files) > 10:
            raise ValidationError("No puedes subir más de 10 archivos a la vez")
        
        total_size = sum(f.size for f in files)
        if total_size > 50 * 1024 * 1024:  # 50MB total
            raise ValidationError("El tamaño total no puede exceder 50MB")
        
        return files


# 4. FORMULARIO CON IMAGEN Y ARCHIVO

class CompleteUploadForm(forms.Form):
    """
    Formulario completo que demuestra diferentes tipos de subidas.
    """
    name = forms.CharField(
        max_length=100,
        label="Nombre",
        help_text="Tu nombre completo"
    )
    avatar = forms.ImageField(
        required=False,
        label="Foto de perfil",
        help_text="Imagen JPG, PNG (máximo 5MB)"
    )
    document = forms.FileField(
        required=False,
        label="Documento",
        help_text="PDF, DOC, TXT (máximo 10MB)"
    )
    gallery = MultipleFileField(
        required=False,
        label="Galería de imágenes",
        help_text="Múltiples imágenes para galería"
    )

    def clean_avatar(self):
        """
        Validación específica para avatar
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError("El avatar no puede ser mayor a 5MB")
            
            # Verificar que sea imagen
            if not avatar.content_type.startswith('image/'):
                raise ValidationError("El archivo debe ser una imagen")
        
        return avatar

    def clean_document(self):
        """
        Validación específica para documento
        """
        document = self.cleaned_data.get('document')
        if document:
            allowed_types = ['application/pdf', 'text/plain', 
                           'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            
            if document.content_type not in allowed_types:
                raise ValidationError("Tipo de documento no permitido")
                
            if document.size > 10 * 1024 * 1024:
                raise ValidationError("El documento no puede ser mayor a 10MB")
        
        return document

    def clean_gallery(self):
        """
        Validación para galería de imágenes
        """
        gallery = self.cleaned_data.get('gallery', [])
        
        for image in gallery:
            if not image.content_type.startswith('image/'):
                raise ValidationError("Todos los archivos de la galería deben ser imágenes")
            
            if image.size > 3 * 1024 * 1024:
                raise ValidationError("Cada imagen de la galería no puede exceder 3MB")
        
        return gallery


# ========================================================================
# FORMULARIOS PARA CLASS-BASED VIEWS
# ========================================================================

class ContactFormCBV(forms.Form):
    """
    Formulario de contacto para usar con FormView
    Ejemplo de la documentación de Class-Based Views
    """
    name = forms.CharField(
        max_length=100,
        label="Nombre completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )
    subject = forms.CharField(
        max_length=200,
        label="Asunto",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mensaje'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...'
        }),
        label="Mensaje"
    )

    def clean_name(self):
        """
        Validación personalizada para el nombre
        """
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise ValidationError("Por favor ingresa tu nombre completo")
        return name

    def send_email(self):
        """
        Método personalizado para enviar el email
        Se llamará desde la vista después de la validación
        """
        # Aquí iría la lógica real de envío de email
        print(f"Enviando email de {self.cleaned_data['name']} <{self.cleaned_data['email']}>")
        print(f"Asunto: {self.cleaned_data['subject']}")
        print(f"Mensaje: {self.cleaned_data['message']}")
        return True