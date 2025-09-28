"""
Custom Upload Handlers for Django File Uploads
Implementación de handlers personalizados según la documentación Django
"""

from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler
from django.http import HttpResponse
import json
import time


class ProgressBarUploadHandler(MemoryFileUploadHandler):
    """
    Handler personalizado que proporciona feedback de progreso
    durante la subida de archivos para widgets AJAX.
    
    Ejemplo directo de la documentación Django.
    """
    
    def __init__(self, request=None):
        super().__init__(request)
        self.progress_id = request.GET.get('progress_id') if request else None
        self.cache_key = None
        if self.progress_id:
            self.cache_key = f"upload_progress_{self.progress_id}"
    
    def new_file(self, *args, **kwargs):
        """
        Llamado cuando se inicia una nueva subida de archivo
        """
        super().new_file(*args, **kwargs)
        if self.cache_key:
            # Inicializar progreso en caché (simulado con variable global para demo)
            global upload_progress
            upload_progress = {
                self.progress_id: {
                    'uploaded': 0,
                    'total': self.content_length,
                    'percent': 0,
                    'status': 'uploading',
                    'filename': kwargs.get('file_name', 'unknown'),
                    'start_time': time.time()
                }
            }
    
    def receive_data_chunk(self, raw_data, start):
        """
        Llamado para cada chunk de datos recibido
        """
        chunk = super().receive_data_chunk(raw_data, start)
        
        if self.cache_key and hasattr(self, 'content_length'):
            # Actualizar progreso
            global upload_progress
            if self.progress_id in upload_progress:
                progress = upload_progress[self.progress_id]
                progress['uploaded'] = start + len(raw_data)
                progress['percent'] = (progress['uploaded'] / progress['total']) * 100
                progress['status'] = 'uploading' if progress['percent'] < 100 else 'completed'
        
        return chunk
    
    def upload_complete(self):
        """
        Llamado cuando la subida está completa
        """
        result = super().upload_complete()
        
        if self.cache_key:
            global upload_progress
            if self.progress_id in upload_progress:
                progress = upload_progress[self.progress_id]
                progress['status'] = 'completed'
                progress['percent'] = 100
                progress['end_time'] = time.time()
                progress['duration'] = progress['end_time'] - progress['start_time']
        
        return result


class QuotaUploadHandler(TemporaryFileUploadHandler):
    """
    Handler que enforza quotas de usuario.
    Ejemplo de handler personalizado para control de límites.
    """
    
    def __init__(self, request=None):
        super().__init__(request)
        self.request = request
        # Quota por usuario (en bytes) - 100MB
        self.user_quota = 100 * 1024 * 1024
    
    def new_file(self, field_name, file_name, content_type, content_length, 
                 charset=None, content_type_extra=None):
        """
        Verificar quota antes de aceptar el archivo
        """
        if self.request and self.request.user.is_authenticated:
            # Calcular uso actual del usuario (simulado)
            current_usage = self.get_user_usage(self.request.user)
            
            if current_usage + content_length > self.user_quota:
                raise Exception(
                    f"Quota excedida. Uso actual: {current_usage/1024/1024:.1f}MB, "
                    f"Límite: {self.user_quota/1024/1024:.1f}MB"
                )
        
        return super().new_file(
            field_name, file_name, content_type, content_length, 
            charset, content_type_extra
        )
    
    def get_user_usage(self, user):
        """
        Calcular uso actual del usuario
        En un caso real, esto consultaría la base de datos
        """
        # Simulamos el cálculo de uso
        from .models import UserUpload
        try:
            uploads = UserUpload.objects.filter(user=user)
            return sum(upload.file_size for upload in uploads)
        except:
            return 0


class CompressUploadHandler(TemporaryFileUploadHandler):
    """
    Handler que comprime archivos automáticamente durante la subida.
    Ejemplo avanzado de procesamiento durante upload.
    """
    
    def __init__(self, request=None):
        super().__init__(request)
        self.compressible_types = [
            'text/plain',
            'text/html',
            'text/css',
            'application/javascript',
            'application/json',
            'text/xml',
            'application/xml'
        ]
    
    def new_file(self, field_name, file_name, content_type, content_length, 
                 charset=None, content_type_extra=None):
        """
        Determinar si el archivo debe comprimirse
        """
        self.should_compress = content_type in self.compressible_types
        self.original_size = content_length
        
        return super().new_file(
            field_name, file_name, content_type, content_length,
            charset, content_type_extra
        )
    
    def receive_data_chunk(self, raw_data, start):
        """
        Procesar chunk de datos (aquí se podría comprimir)
        """
        # En un caso real, aquí comprimiríamos los datos
        if self.should_compress:
            # Simular compresión (en realidad no comprimimos para simplicidad)
            pass
        
        return super().receive_data_chunk(raw_data, start)
    
    def upload_complete(self):
        """
        Finalizar procesamiento
        """
        result = super().upload_complete()
        
        if self.should_compress and hasattr(self, 'file'):
            # Aquí marcaríamos que el archivo fue comprimido
            # En un caso real, actualizaríamos metadatos
            pass
        
        return result


# Variable global para simular caché de progreso
# En producción se usaría Redis, Memcached, etc.
upload_progress = {}


def get_upload_progress(request):
    """
    Vista AJAX para obtener el progreso de subida
    """
    progress_id = request.GET.get('progress_id')
    if progress_id and progress_id in upload_progress:
        return HttpResponse(
            json.dumps(upload_progress[progress_id]),
            content_type='application/json'
        )
    return HttpResponse(
        json.dumps({'error': 'Progress ID not found'}),
        content_type='application/json',
        status=404
    )