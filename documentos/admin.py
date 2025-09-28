from django.contrib import admin
from .models import Car, CarWithCustomStorage, Document, Report, Profile


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'has_photo', 'has_specs']
    list_filter = ['price']
    search_fields = ['name']
    
    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Tiene Foto'
    
    def has_specs(self, obj):
        return bool(obj.specs)
    has_specs.boolean = True
    has_specs.short_description = 'Tiene Especificaciones'


@admin.register(CarWithCustomStorage)
class CarWithCustomStorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'has_photo']
    list_filter = ['price']
    search_fields = ['name']
    
    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Tiene Foto'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'has_file']
    list_filter = ['created_at']
    search_fields = ['title']
    date_hierarchy = 'created_at'
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.boolean = True
    has_file.short_description = 'Tiene Archivo'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'generated_at', 'has_file']
    list_filter = ['generated_at']
    search_fields = ['name']
    date_hierarchy = 'generated_at'
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.boolean = True
    has_file.short_description = 'Tiene Archivo'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'has_avatar', 'has_resume']
    search_fields = ['username']
    
    def has_avatar(self, obj):
        return bool(obj.avatar)
    has_avatar.boolean = True
    has_avatar.short_description = 'Tiene Avatar'
    
    def has_resume(self, obj):
        return bool(obj.resume)
    has_resume.boolean = True
    has_resume.short_description = 'Tiene CV'
