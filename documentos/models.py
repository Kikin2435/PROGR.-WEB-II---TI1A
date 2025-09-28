from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import storages
from django.conf import settings
from django.utils.functional import LazyObject

# Create your models here.

class Car(models.Model):
    """
    Example Car model demonstrating ImageField and FileField usage
    as described in Django documentation.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to="cars")
    specs = models.FileField(upload_to="specs")
    
    def __str__(self):
        return self.name


# Custom storage for specific locations
fs = FileSystemStorage(location="/media/photos")

class CarWithCustomStorage(models.Model):
    """
    Example model using custom FileSystemStorage
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(storage=fs)
    
    def __str__(self):
        return f"Custom Storage Car: {self.name}"


# Storage callable examples
def select_storage():
    """
    Callable that returns different storage based on DEBUG setting
    """
    if settings.DEBUG:
        return FileSystemStorage(location="media/local")
    else:
        return FileSystemStorage(location="media/production")


def select_storage_from_settings():
    """
    Callable that uses storage from STORAGES setting
    """
    return storages["default"]


class Document(models.Model):
    """
    Document model demonstrating callable storage
    """
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents", storage=select_storage)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


# LazyObject storage for testing
class CustomStorage(LazyObject):
    """
    Lazy storage object for testing scenarios
    """
    def _setup(self):
        self._wrapped = storages["default"]


custom_storage = CustomStorage()

class Report(models.Model):
    """
    Report model using lazy storage object
    """
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="reports", storage=custom_storage)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    User profile with avatar image
    """
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(
        upload_to="avatars", 
        null=True, 
        blank=True,
        help_text="Upload a profile picture"
    )
    resume = models.FileField(
        upload_to="resumes",
        null=True,
        blank=True,
        help_text="Upload your resume (PDF preferred)"
    )
    
    def __str__(self):
        return self.username


# ========================================================================
# MODELOS PARA FILE UPLOADS - Ejemplos de la documentación Django
# ========================================================================

def user_directory_path(instance, filename):
    """
    Función callable para generar paths dinámicos
    Los archivos se guardarán en MEDIA_ROOT/user_<id>/<filename>
    """
    return f'user_{instance.user.id}/{filename}'


class UserUpload(models.Model):
    """
    Modelo para demostrar uploads con path dinámico
    """
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='uploads'
    )
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=user_directory_path,
        help_text="Archivo del usuario (se organizará por carpetas)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Upload de Usuario'
        verbose_name_plural = 'Uploads de Usuarios'
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    def save(self, *args, **kwargs):
        """
        Override para guardar el tamaño del archivo
        """
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class Gallery(models.Model):
    """
    Modelo para galería de imágenes con múltiples archivos
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """
    Modelo individual para cada imagen de la galería
    Usado para simular subida múltiple con ModelForm
    """
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='gallery/',
        help_text="Imagen para la galería"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Descripción opcional de la imagen"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.gallery.name} - {self.caption or 'Sin título'}"


class FileUploadDemo(models.Model):
    """
    Modelo de demostración para diferentes tipos de archivos
    """
    CATEGORY_CHOICES = [
        ('document', 'Documento'),
        ('image', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Otro'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='document'
    )
    file = models.FileField(
        upload_to='uploads/%Y/%m/',
        help_text="Archivo organizado por fecha"
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        help_text="Miniatura opcional"
    )
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloads = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Archivo de Demostración'
        verbose_name_plural = 'Archivos de Demostración'
    
    def __str__(self):
        return self.title
    
    def get_file_size(self):
        """
        Retorna el tamaño del archivo en formato legible
        """
        if self.file:
            size = self.file.size
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024**2:
                return f"{size/1024:.1f} KB"
            elif size < 1024**3:
                return f"{size/(1024**2):.1f} MB"
            else:
                return f"{size/(1024**3):.1f} GB"
        return "0 bytes"
