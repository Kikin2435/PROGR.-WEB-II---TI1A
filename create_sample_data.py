"""
Script para crear datos de ejemplo para demostrar formularios Django
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expediente.settings')
django.setup()

from documentos.models import Car, Document, Profile


def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear algunos vehículos de ejemplo
    cars_data = [
        {
            'name': 'Toyota Camry 2023',
            'price': Decimal('28500.00')
        },
        {
            'name': 'Honda Civic 2024',
            'price': Decimal('24000.00')
        },
        {
            'name': 'BMW X5 2023',
            'price': Decimal('67500.00')
        }
    ]
    
    for car_data in cars_data:
        car, created = Car.objects.get_or_create(
            name=car_data['name'],
            defaults={'price': car_data['price']}
        )
        if created:
            print(f"✅ Vehículo creado: {car.name}")
        else:
            print(f"⚠️ Vehículo ya existe: {car.name}")
    
    # Crear algunos documentos de ejemplo
    documents_data = [
        'Manual de Usuario',
        'Políticas de la Empresa',
        'Guía de Instalación'
    ]
    
    for doc_title in documents_data:
        doc, created = Document.objects.get_or_create(
            title=doc_title
        )
        if created:
            print(f"✅ Documento creado: {doc.title}")
        else:
            print(f"⚠️ Documento ya existe: {doc.title}")
    
    # Crear algunos perfiles de ejemplo
    profiles_data = [
        'juan_perez',
        'maria_garcia',
        'carlos_lopez'
    ]
    
    for username in profiles_data:
        profile, created = Profile.objects.get_or_create(
            username=username
        )
        if created:
            print(f"✅ Perfil creado: {profile.username}")
        else:
            print(f"⚠️ Perfil ya existe: {profile.username}")
    
    print("\n🎉 Datos de ejemplo creados exitosamente!")
    print(f"📊 Total: {Car.objects.count()} vehículos, {Document.objects.count()} documentos, {Profile.objects.count()} perfiles")


if __name__ == "__main__":
    create_sample_data()