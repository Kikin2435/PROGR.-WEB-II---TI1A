#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# Add the Django project to path
sys.path.append('C:\\Users\\Kikin\\OneDrive\\Desktop\\ITSUR\\7\\Web 2\\Proyecto expediente\\expediente')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expediente.settings')
django.setup()

from django.contrib.auth.models import User
from documentos.models import Car, Document, Profile

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Admin user created: admin/admin123")
    
    # Clear existing data
    Car.objects.all().delete()
    Document.objects.all().delete()
    Profile.objects.all().delete()
    print("🗑️ Cleared existing data")
    
    # Create sample cars with valid decimal prices
    cars_data = [
        {'name': 'Toyota Camry', 'price': Decimal('25000.00')},
        {'name': 'Honda Civic', 'price': Decimal('22000.00')},
        {'name': 'Ford Mustang', 'price': Decimal('35000.00')},
    ]
    
    for car_data in cars_data:
        car = Car.objects.create(**car_data)
        print(f"✅ Created car: {car.name} - ${car.price}")
    
    # Create sample documents
    docs_data = [
        {'title': 'Manual de Usuario'},
        {'title': 'Especificaciones'},
        {'title': 'Garantía'},
    ]
    
    for doc_data in docs_data:
        doc = Document.objects.create(**doc_data)
        print(f"✅ Created document: {doc.title}")
    
    # Create sample profiles
    profiles_data = [
        {'username': 'developer1'},
        {'username': 'designer2'},
        {'username': 'manager3'},
    ]
    
    for profile_data in profiles_data:
        if not Profile.objects.filter(username=profile_data['username']).exists():
            profile = Profile.objects.create(**profile_data)
            print(f"✅ Created profile: {profile.username}")
    
    print("\n🎉 Sample data created successfully!")
    print(f"📊 Cars: {Car.objects.count()}")
    print(f"📄 Documents: {Document.objects.count()}")
    print(f"👤 Profiles: {Profile.objects.count()}")
    print(f"👥 Users: {User.objects.count()}")

if __name__ == '__main__':
    create_sample_data()