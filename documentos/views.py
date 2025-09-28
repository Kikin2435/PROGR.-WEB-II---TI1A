from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from pathlib import Path
from PIL import Image
import json

from .models import Car, Document, Profile
from .forms import (
    NameForm, ContactForm, CarForm, DocumentForm, 
    ProfileForm, SearchForm, DynamicFieldForm
)


def index(request):
    """
    Index view showing file handling examples
    """
    cars = Car.objects.all()
    documents = Document.objects.all()
    profiles = Profile.objects.all()
    
    context = {
        'cars': cars,
        'documents': documents,
        'profiles': profiles,
    }
    return render(request, 'documentos/index.html', context)


def car_list(request):
    """
    List all cars with their photos and specs
    """
    cars = Car.objects.all()
    return render(request, 'documentos/car_list.html', {'cars': cars})


def car_detail(request, pk):
    """
    Show car details with file information
    Demonstrates the Django file API usage from the documentation
    """
    car = get_object_or_404(Car, pk=pk)
    
    # Example of file API usage as shown in Django docs
    file_info = {}
    
    if car.photo:
        file_info['photo'] = {
            'name': car.photo.name,
            'path': car.photo.path if hasattr(car.photo, 'path') else None,
            'url': car.photo.url,
            'size': car.photo.size,
            'width': car.photo.width if hasattr(car.photo, 'width') else None,
            'height': car.photo.height if hasattr(car.photo, 'height') else None,
        }
    
    if car.specs:
        file_info['specs'] = {
            'name': car.specs.name,
            'path': car.specs.path if hasattr(car.specs, 'path') else None,
            'url': car.specs.url,
            'size': car.specs.size,
        }
    
    context = {
        'car': car,
        'file_info': file_info,
    }
    return render(request, 'documentos/car_detail.html', context)


@csrf_exempt
def upload_file(request):
    """
    Example view for handling file uploads
    Demonstrates various file handling techniques from Django docs
    """
    if request.method == 'POST':
        try:
            # Example 1: Using default storage directly
            if 'default_file' in request.FILES:
                uploaded_file = request.FILES['default_file']
                # Save using default storage
                path = default_storage.save(
                    f"uploads/{uploaded_file.name}", 
                    ContentFile(uploaded_file.read())
                )
                
                return JsonResponse({
                    'success': True,
                    'message': f'File saved to {path}',
                    'size': default_storage.size(path),
                    'exists': default_storage.exists(path),
                })
            
            # Example 2: Save to model with FileField
            if 'car_name' in request.POST and 'car_photo' in request.FILES:
                car = Car.objects.create(
                    name=request.POST['car_name'],
                    price=float(request.POST.get('car_price', 0)),
                    photo=request.FILES['car_photo']
                )
                
                if 'car_specs' in request.FILES:
                    car.specs = request.FILES['car_specs']
                    car.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Car "{car.name}" created successfully',
                    'car_id': car.id,
                    'photo_url': car.photo.url if car.photo else None,
                })
            
            # Example 3: Create File object from existing file
            if 'external_file_path' in request.POST:
                file_path = Path(request.POST['external_file_path'])
                if file_path.exists():
                    car_name = request.POST.get('car_name_external', 'External Car')
                    car = Car.objects.create(
                        name=car_name,
                        price=float(request.POST.get('car_price', 0))
                    )
                    
                    # Save external file to FileField as shown in docs
                    with file_path.open(mode="rb") as f:
                        car.specs = File(f, name=file_path.name)
                        car.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'External file saved for car "{car.name}"',
                        'specs_url': car.specs.url,
                    })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # GET request - show upload form
    return render(request, 'documentos/upload.html')


def file_operations_demo(request):
    """
    Demonstrates various file operations from Django documentation
    """
    operations_log = []
    
    try:
        # Create a sample file using ContentFile
        content = ContentFile(b"Sample file content for demo")
        path = default_storage.save("demo/sample.txt", content)
        operations_log.append(f"Created file at: {path}")
        
        # Check file exists
        exists = default_storage.exists(path)
        operations_log.append(f"File exists: {exists}")
        
        # Get file size
        size = default_storage.size(path)
        operations_log.append(f"File size: {size} bytes")
        
        # Read file content
        with default_storage.open(path) as f:
            content = f.read()
            operations_log.append(f"File content: {content}")
        
        # Clean up - delete the demo file
        default_storage.delete(path)
        operations_log.append("Demo file deleted")
        
    except Exception as e:
        operations_log.append(f"Error: {str(e)}")
    
    return JsonResponse({
        'operations': operations_log
    })


# ====== NUEVAS VISTAS PARA FORMULARIOS ======

def get_name(request):
    """
    Vista que maneja el formulario básico NameForm.
    Ejemplo exacto de la documentación de Django.
    """
    if request.method == "POST":
        # Crear instancia del formulario con datos del request
        form = NameForm(request.POST)
        # Verificar si es válido
        if form.is_valid():
            # Procesar los datos en form.cleaned_data
            name = form.cleaned_data['your_name']
            messages.success(request, f"¡Hola {name}! Gracias por enviar tu nombre.")
            # Redirigir a una nueva URL
            return HttpResponseRedirect("/documentos/thanks/")
    else:
        # Si es GET, crear formulario vacío
        form = NameForm()
    
    return render(request, "documentos/forms/name_form.html", {"form": form})


def contact_form_view(request):
    """
    Vista para el formulario de contacto.
    Demuestra manejo más complejo con validación y envío de email.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Obtener datos validados
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]
            
            # Preparar destinatarios
            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)
            
            try:
                # Enviar email (en un caso real)
                # send_mail(subject, message, sender, recipients)
                
                # Para demo, solo mostrar mensaje de éxito
                messages.success(
                    request, 
                    f"Mensaje '{subject}' enviado correctamente desde {sender}"
                )
                return redirect('documentos:contact_success')
                
            except Exception as e:
                messages.error(request, f"Error al enviar mensaje: {str(e)}")
    else:
        form = ContactForm()
    
    return render(request, "documentos/forms/contact_form.html", {"form": form})


def create_car(request):
    """
    Vista para crear un nuevo vehículo usando ModelForm
    """
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(
                request, 
                f"Vehículo '{car.name}' creado exitosamente."
            )
            return redirect('documentos:car_detail', pk=car.pk)
    else:
        form = CarForm()
    
    return render(request, "documentos/forms/car_form.html", {
        "form": form,
        "title": "Agregar Nuevo Vehículo"
    })


def edit_car(request, pk):
    """
    Vista para editar un vehículo existente
    """
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            messages.success(
                request, 
                f"Vehículo '{car.name}' actualizado exitosamente."
            )
            return redirect('documentos:car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    
    return render(request, "documentos/forms/car_form.html", {
        "form": form,
        "title": f"Editar {car.name}",
        "car": car
    })


def create_document(request):
    """
    Vista para crear un nuevo documento
    """
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(
                request, 
                f"Documento '{document.title}' subido exitosamente."
            )
            return redirect('documentos:index')
    else:
        form = DocumentForm()
    
    return render(request, "documentos/forms/document_form.html", {
        "form": form,
        "title": "Subir Nuevo Documento"
    })


def create_profile(request):
    """
    Vista para crear un nuevo perfil
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            messages.success(
                request, 
                f"Perfil '{profile.username}' creado exitosamente."
            )
            return redirect('documentos:index')
    else:
        form = ProfileForm()
    
    return render(request, "documentos/forms/profile_form.html", {
        "form": form,
        "title": "Crear Nuevo Perfil"
    })


def search_view(request):
    """
    Vista de búsqueda que demuestra formularios con validación compleja
    """
    results = []
    form = SearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        search_in = form.cleaned_data['search_in']
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        # Realizar búsqueda según los parámetros
        if search_in in ['cars', 'all']:
            car_query = Car.objects.filter(name__icontains=query)
            if min_price:
                car_query = car_query.filter(price__gte=min_price)
            if max_price:
                car_query = car_query.filter(price__lte=max_price)
            results.extend([('car', car) for car in car_query])
        
        if search_in in ['documents', 'all']:
            doc_query = Document.objects.filter(title__icontains=query)
            results.extend([('document', doc) for doc in doc_query])
        
        if search_in in ['profiles', 'all']:
            profile_query = Profile.objects.filter(username__icontains=query)
            results.extend([('profile', profile) for profile in profile_query])
    
    return render(request, "documentos/forms/search.html", {
        "form": form,
        "results": results,
        "query": form.cleaned_data.get('query') if form.is_valid() else None
    })


def dynamic_form_view(request):
    """
    Vista que demuestra formularios con campos dinámicos
    """
    show_advanced = request.GET.get('advanced') == 'true'
    
    if request.method == "POST":
        form = DynamicFieldForm(request.POST, show_advanced=show_advanced)
        if form.is_valid():
            # Procesar datos del formulario
            basic_field = form.cleaned_data['basic_field']
            messages.success(request, f"Formulario procesado: {basic_field}")
            
            if show_advanced:
                advanced_field = form.cleaned_data.get('advanced_field')
                color = form.cleaned_data.get('color_preference')
                if advanced_field:
                    messages.info(request, f"Campo avanzado: {advanced_field}")
                if color:
                    messages.info(request, f"Color seleccionado: {color}")
    else:
        form = DynamicFieldForm(show_advanced=show_advanced)
    
    return render(request, "documentos/forms/dynamic_form.html", {
        "form": form,
        "show_advanced": show_advanced
    })


def form_examples_index(request):
    """
    Vista índice que muestra todos los ejemplos de formularios disponibles
    """
    return render(request, "documentos/forms/examples_index.html")


def thanks_view(request):
    """
    Página de agradecimiento después de enviar formularios
    """
    return render(request, "documentos/forms/thanks.html")


def contact_success_view(request):
    """
    Página de éxito para formulario de contacto
    """
    return render(request, "documentos/forms/contact_success.html")


# ========================================================================
# VISTAS PARA FILE UPLOADS - Implementación documentación Django
# ========================================================================

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .upload_handlers import ProgressBarUploadHandler, QuotaUploadHandler
from .forms import (
    UploadFileForm, ModelFormWithFileField, FileFieldForm, 
    CompleteUploadForm
)
from .models import UserUpload, Gallery, GalleryImage, FileUploadDemo
import os
import uuid


def handle_uploaded_file(f):
    """
    Función auxiliar para manejar archivos subidos.
    Ejemplo directo de la documentación Django.
    """
    # Generar nombre único para evitar colisiones
    filename = f"uploaded_{uuid.uuid4().hex}_{f.name}"
    file_path = os.path.join("uploads", filename)
    
    # Asegurar que el directorio existe
    full_path = default_storage.path(file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Escribir archivo usando chunks para archivos grandes
    with default_storage.open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path


def upload_file_basic(request):
    """
    Vista básica para subida de archivos.
    Implementación exacta del ejemplo de la documentación Django.
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Manejar archivo subido
            file_path = handle_uploaded_file(request.FILES["file"])
            
            # Crear registro de demostración
            FileUploadDemo.objects.create(
                title=form.cleaned_data['title'],
                file=file_path,
                category='document',
                description=f"Archivo subido: {request.FILES['file'].name}"
            )
            
            messages.success(
                request, 
                f"Archivo '{request.FILES['file'].name}' subido exitosamente."
            )
            return HttpResponseRedirect("/documentos/uploads/success/")
    else:
        form = UploadFileForm()
    
    return render(request, "documentos/uploads/basic_upload.html", {"form": form})


def upload_file_model(request):
    """
    Vista usando ModelForm para manejar archivos con modelo.
    El archivo se guarda automáticamente en el modelo.
    """
    if request.method == "POST":
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # El archivo se guarda automáticamente
            document = form.save()
            messages.success(
                request, 
                f"Documento '{document.title}' guardado exitosamente."
            )
            return HttpResponseRedirect("/documentos/uploads/success/")
    else:
        form = ModelFormWithFileField()
    
    return render(request, "documentos/uploads/model_upload.html", {"form": form})


def upload_file_manual_model(request):
    """
    Vista que construye objeto manualmente asignando archivo.
    Ejemplo de la documentación para construcción manual.
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Construir objeto manualmente
            instance = FileUploadDemo(
                title=form.cleaned_data['title'],
                file=request.FILES["file"],
                category='document'
            )
            instance.save()
            
            messages.success(
                request, 
                f"Archivo '{instance.title}' guardado manualmente."
            )
            return HttpResponseRedirect("/documentos/uploads/success/")
    else:
        form = UploadFileForm()
    
    return render(request, "documentos/uploads/manual_upload.html", {"form": form})


class FileFieldFormView(FormView):
    """
    Vista basada en clase para manejar múltiples archivos.
    Implementación del ejemplo de la documentación Django.
    """
    form_class = FileFieldForm
    template_name = "documentos/uploads/multiple_upload.html"
    success_url = "/documentos/uploads/success/"

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        title = form.cleaned_data["title"]
        
        # Crear galería para agrupar los archivos
        gallery = Gallery.objects.create(
            name=title,
            description=f"Galería creada con {len(files)} archivos"
        )
        
        # Procesar cada archivo
        for f in files:
            # Determinar si es imagen
            is_image = f.content_type.startswith('image/')
            
            if is_image:
                # Guardar como imagen en galería
                GalleryImage.objects.create(
                    gallery=gallery,
                    image=f,
                    caption=f.name
                )
            else:
                # Guardar como archivo general
                FileUploadDemo.objects.create(
                    title=f.name,
                    file=f,
                    category='document',
                    description=f"Archivo de la galería: {title}"
                )
        
        messages.success(
            self.request, 
            f"Se subieron {len(files)} archivos en la galería '{title}'"
        )
        
        return super().form_valid(form)


def complete_upload_view(request):
    """
    Vista que demuestra formulario completo con diferentes tipos de archivos
    """
    if request.method == "POST":
        form = CompleteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            avatar = form.cleaned_data.get('avatar')
            document = form.cleaned_data.get('document')
            gallery_images = form.cleaned_data.get('gallery', [])
            
            # Crear usuario upload si hay archivos
            if avatar or document or gallery_images:
                # Crear o obtener usuario para demo
                from django.contrib.auth.models import User
                user, created = User.objects.get_or_create(
                    username=f"demo_user_{name.replace(' ', '_').lower()}",
                    defaults={'email': f"{name.replace(' ', '_').lower()}@example.com"}
                )
                
                results = []
                
                # Procesar avatar
                if avatar:
                    upload = UserUpload.objects.create(
                        user=user,
                        title=f"Avatar de {name}",
                        file=avatar
                    )
                    results.append(f"Avatar subido: {upload.file.name}")
                
                # Procesar documento
                if document:
                    upload = UserUpload.objects.create(
                        user=user,
                        title=f"Documento de {name}",
                        file=document
                    )
                    results.append(f"Documento subido: {upload.file.name}")
                
                # Procesar galería
                if gallery_images:
                    gallery = Gallery.objects.create(
                        name=f"Galería de {name}",
                        description=f"Galería con {len(gallery_images)} imágenes"
                    )
                    
                    for img in gallery_images:
                        GalleryImage.objects.create(
                            gallery=gallery,
                            image=img,
                            caption=img.name
                        )
                    
                    results.append(f"Galería creada con {len(gallery_images)} imágenes")
                
                messages.success(
                    request, 
                    f"Upload completo para {name}: " + ", ".join(results)
                )
            else:
                messages.info(request, f"Perfil de {name} registrado sin archivos")
            
            return HttpResponseRedirect("/documentos/uploads/success/")
    else:
        form = CompleteUploadForm()
    
    return render(request, "documentos/uploads/complete_upload.html", {"form": form})


@csrf_exempt
def upload_with_progress(request):
    """
    Vista que usa handlers personalizados para mostrar progreso.
    Demuestra modificación de upload handlers según documentación.
    """
    # Modificar upload handlers antes de acceder a request.POST
    if request.method == "POST":
        progress_id = request.GET.get('progress_id', str(uuid.uuid4()))
        request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
        
        return _upload_with_progress_protected(request, progress_id)
    else:
        # Generar ID único para el progreso
        progress_id = str(uuid.uuid4())
        form = UploadFileForm()
        
        return render(request, "documentos/uploads/progress_upload.html", {
            "form": form,
            "progress_id": progress_id
        })


@csrf_protect
def _upload_with_progress_protected(request, progress_id):
    """
    Función protegida por CSRF que procesa la subida con progreso
    """
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_path = handle_uploaded_file(request.FILES["file"])
        
        FileUploadDemo.objects.create(
            title=form.cleaned_data['title'],
            file=file_path,
            category='document',
            description=f"Archivo con progreso: {request.FILES['file'].name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': f"Archivo '{request.FILES['file'].name}' subido exitosamente.",
            'progress_id': progress_id
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
            'progress_id': progress_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class UploadWithQuotaView(View):
    """
    Vista basada en clase que usa handler de quota.
    Ejemplo de modificación de handlers en clase.
    """
    def setup(self, request, *args, **kwargs):
        # Modificar handlers antes de procesar
        if request.method == "POST":
            request.upload_handlers.insert(0, QuotaUploadHandler(request))
        super().setup(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_path = handle_uploaded_file(request.FILES["file"])
                
                # Crear registro para el usuario autenticado
                if request.user.is_authenticated:
                    UserUpload.objects.create(
                        user=request.user,
                        title=form.cleaned_data['title'],
                        file=file_path
                    )
                
                return JsonResponse({
                    'success': True,
                    'message': f"Archivo '{request.FILES['file'].name}' subido con control de quota."
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        user_usage = 0
        quota = 100 * 1024 * 1024  # 100MB
        
        if request.user.is_authenticated:
            uploads = UserUpload.objects.filter(user=request.user)
            user_usage = sum(upload.file_size for upload in uploads)
        
        return render(request, "documentos/uploads/quota_upload.html", {
            "form": form,
            "user_usage": user_usage,
            "quota": quota,
            "usage_percent": (user_usage / quota * 100) if quota > 0 else 0
        })


def upload_success(request):
    """
    Página de éxito para uploads
    """
    return render(request, "documentos/uploads/success.html")


def upload_examples_index(request):
    """
    Índice de ejemplos de file uploads
    """
    return render(request, "documentos/uploads/index.html")


# Vista AJAX para obtener progreso
def get_upload_progress(request):
    """
    Vista AJAX para obtener el progreso de subida
    """
    from .upload_handlers import get_upload_progress
    return get_upload_progress(request)


# ========================================================================
# CLASS-BASED VIEWS - Vistas basadas en clases
# ========================================================================

from django.views.generic import FormView, CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages

from .forms import ContactFormCBV

class CBVIndexView(TemplateView):
    """
    Vista índice para mostrar todos los ejemplos de Class-Based Views
    """
    template_name = 'documentos/cbv/cbv_index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Django Class-Based Views - Índice'
        context['description'] = 'Ejemplos completos de vistas basadas en clases'
        return context

class ContactFormView(FormView):
    """
    FormView básico para formulario de contacto
    Ejemplo de la documentación Django sobre Class-Based Views
    """
    template_name = 'documentos/cbv/contact_form.html'
    form_class = ContactFormCBV
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario es válido
        """
        # Procesar el formulario
        form.send_email()
        
        # Agregar mensaje de éxito
        messages.success(
            self.request, 
            f'¡Gracias {form.cleaned_data["name"]}! Tu mensaje ha sido enviado correctamente.'
        )
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Agregar contexto adicional al template
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Formulario de Contacto - CBV'
        context['description'] = 'Ejemplo de FormView con Class-Based Views'
        return context


class CarListView(ListView):
    """
    Vista para listar todos los vehículos
    """
    model = Car
    template_name = 'documentos/cbv/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10

    def get_queryset(self):
        """
        Personalizar el queryset
        """
        queryset = super().get_queryset()
        # Ordenar por precio (más caros primero)
        return queryset.order_by('-price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Lista de Vehículos'
        return context


class CarCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear nuevos vehículos usando CreateView
    Requiere autenticación para crear vehículos
    """
    model = Car
    form_class = CarForm
    template_name = 'documentos/cbv/car_form.html'
    success_url = reverse_lazy('car_list_cbv')
    login_url = '/admin/login/'  # URL de login por defecto

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario es válido
        """
        messages.success(self.request, '¡Vehículo creado exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Crear Vehículo'
        context['form_action'] = 'Crear'
        return context


class CarUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar vehículos existentes
    Requiere autenticación para editar vehículos
    """
    model = Car
    form_class = CarForm
    template_name = 'documentos/cbv/car_form.html'
    success_url = reverse_lazy('car_list_cbv')
    login_url = '/admin/login/'  # URL de login por defecto

    def form_valid(self, form):
        messages.success(self.request, '¡Vehículo actualizado exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Actualizar Vehículo'
        context['form_action'] = 'Actualizar'
        return context


class CarDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar vehículos
    Requiere autenticación para eliminar vehículos
    """
    model = Car
    template_name = 'documentos/cbv/car_confirm_delete.html'
    success_url = reverse_lazy('car_list_cbv')
    login_url = '/admin/login/'  # URL de login por defecto

    def delete(self, request, *args, **kwargs):
        """
        Personalizar el proceso de eliminación
        """
        car = self.get_object()
        messages.success(request, f'¡Vehículo "{car.name}" eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Eliminar Vehículo'
        return context


# ========================================================================
# MIXINS PARA CONTENT NEGOTIATION
# ========================================================================

class JSONResponseMixin:
    """
    Mixin para retornar respuestas JSON
    """
    def dispatch(self, request, *args, **kwargs):
        # Guardar si la petición es AJAX
        self.is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax:
            data = {
                'pk': self.object.pk,
                'success': True,
                'message': 'Operación exitosa'
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return response


class AjaxableResponseMixin:
    """
    Mixin para manejar respuestas AJAX según la documentación Django
    """
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        else:
            return response


# Vistas que combinan CRUD con AJAX
class CarCreateAjaxView(JSONResponseMixin, LoginRequiredMixin, CreateView):
    """
    Vista de creación que maneja tanto requests HTTP como AJAX
    Requiere autenticación
    """
    model = Car
    form_class = CarForm
    template_name = 'documentos/cbv/car_form.html'
    success_url = reverse_lazy('car_list_cbv')
    login_url = '/admin/login/'

    def form_valid(self, form):
        messages.success(self.request, '¡Vehículo creado exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Crear Vehículo (AJAX)'
        context['form_action'] = 'Crear'
        return context


class CarUpdateAjaxView(JSONResponseMixin, LoginRequiredMixin, UpdateView):
    """
    Vista de actualización que maneja tanto requests HTTP como AJAX
    Requiere autenticación
    """
    model = Car
    form_class = CarForm
    template_name = 'documentos/cbv/car_form.html'
    success_url = reverse_lazy('car_list_cbv')
    login_url = '/admin/login/'

    def form_valid(self, form):
        messages.success(self.request, '¡Vehículo actualizado exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Actualizar Vehículo (AJAX)'
        context['form_action'] = 'Actualizar'
        return context


class ContactSuccessView(FormView):
    """
    Vista de éxito para el formulario de contacto
    """
    template_name = 'documentos/cbv/contact_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mensaje Enviado'
        return context
