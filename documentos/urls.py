from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    # URLs originales
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('upload/', views.upload_file, name='upload_file'),
    
    # URLs para formularios
    path('forms/', views.form_examples_index, name='form_examples'),
    path('forms/name/', views.get_name, name='name_form'),
    path('forms/contact/', views.contact_form_view, name='contact_form'),
    path('forms/search/', views.search_view, name='search'),
    path('forms/dynamic/', views.dynamic_form_view, name='dynamic_form'),
    
    # CRUD para modelos con formularios
    path('cars/create/', views.create_car, name='create_car'),
    path('cars/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('documents/create/', views.create_document, name='create_document'),
    path('profiles/create/', views.create_profile, name='create_profile'),
    
    # Páginas de éxito para formularios
    path('thanks/', views.thanks_view, name='thanks'),
    path('contact-success/', views.contact_success_view, name='contact_success'),
    
    # ========================================================================
    # URLs PARA FILE UPLOADS - Implementación documentación Django
    # ========================================================================
    
    # Índice de ejemplos de uploads
    path('uploads/', views.upload_examples_index, name='upload_index'),
    
    # Upload básico - ejemplo directo de la documentación
    path('uploads/basic/', views.upload_file_basic, name='upload_basic'),
    
    # Upload con ModelForm - guardado automático
    path('uploads/model/', views.upload_file_model, name='upload_model'),
    
    # Upload manual - construcción manual del objeto
    path('uploads/manual/', views.upload_file_manual_model, name='upload_manual'),
    
    # Upload múltiple - widget personalizado
    path('uploads/multiple/', views.FileFieldFormView.as_view(), name='upload_multiple'),
    
    # Upload completo - imagen + documento + galería
    path('uploads/complete/', views.complete_upload_view, name='upload_complete'),
    
    # Upload con progreso - handler personalizado
    path('uploads/progress/', views.upload_with_progress, name='upload_progress'),
    
    # Upload con quota - control de límites
    path('uploads/quota/', views.UploadWithQuotaView.as_view(), name='upload_quota'),
    
    # Página de éxito para uploads
    path('uploads/success/', views.upload_success, name='upload_success'),
    
    # AJAX endpoint para obtener progreso de upload
    path('uploads/progress/', views.get_upload_progress, name='upload_progress_api'),
    
    # ========================================================================
    # URLs PARA CLASS-BASED VIEWS - Vistas basadas en clases
    # ========================================================================
    
    # Índice de Class-Based Views
    path('cbv/', views.CBVIndexView.as_view(), name='cbv_index'),
    
    # FormView - Formulario de contacto CBV
    path('cbv/contact/', views.ContactFormView.as_view(), name='contact_form_cbv'),
    path('cbv/contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    
    # ListView - Lista de vehículos
    path('cbv/cars/', views.CarListView.as_view(), name='car_list_cbv'),
    
    # CreateView - Crear vehículo
    path('cbv/cars/create/', views.CarCreateView.as_view(), name='car_create_cbv'),
    
    # UpdateView - Actualizar vehículo
    path('cbv/cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update_cbv'),
    
    # DeleteView - Eliminar vehículo
    path('cbv/cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete_cbv'),
    
    # Vistas AJAX - Combinación de CBV con AJAX
    path('cbv/cars/create/ajax/', views.CarCreateAjaxView.as_view(), name='car_create_ajax'),
    path('cbv/cars/<int:pk>/update/ajax/', views.CarUpdateAjaxView.as_view(), name='car_update_ajax'),
]