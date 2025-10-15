from django.urls import path
from ubicaciones import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-municipios/', views.get_municipios, name='get_municipios'),
]