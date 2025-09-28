# 📝 Guía Completa: Trabajar con Formularios en Django

## 🌟 **¿Qué Hemos Implementado?**

Hemos creado un sistema completo que demuestra **todos los conceptos fundamentales** de formularios en Django según la documentación oficial.

## 📋 **Conceptos Implementados**

### **1. Formularios Básicos (Form)**
```python
class NameForm(forms.Form):
    your_name = forms.CharField(label="Tu nombre", max_length=100)
```

**Características:**
- ✅ Campos creados manualmente
- ✅ Validación automática de longitud
- ✅ Control total sobre el formulario

### **2. ModelForm - Formularios desde Modelos**
```python
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'price', 'photo', 'specs']
```

**Características:**
- ✅ Generado automáticamente desde modelo
- ✅ Manejo de archivos (ImageField, FileField)
- ✅ Validación personalizada
- ✅ Labels y help_text personalizados

### **3. Tipos de Campos Demostrados**

| Campo | Uso | Ejemplo |
|-------|-----|---------|
| `CharField` | Texto simple | Nombres, títulos |
| `EmailField` | Emails | Direcciones de correo |
| `BooleanField` | Casillas de verificación | Opciones sí/no |
| `DecimalField` | Números decimales | Precios |
| `ChoiceField` | Opciones predefinidas | Listas desplegables |
| `ImageField` | Imágenes | Fotos, avatares |
| `FileField` | Archivos | PDFs, documentos |

### **4. Widgets Personalizados**
```python
message = forms.CharField(widget=forms.Textarea)
price = forms.DecimalField(widget=forms.NumberInput(attrs={'step': '0.01'}))
```

## 🔄 **Flujo GET/POST Implementado**

### **GET Request (Mostrar Formulario)**
```python
def get_name(request):
    if request.method == "GET":
        form = NameForm()  # Formulario unbound (vacío)
    return render(request, "template.html", {"form": form})
```

### **POST Request (Procesar Datos)**
```python
def get_name(request):
    if request.method == "POST":
        form = NameForm(request.POST)  # Formulario bound (con datos)
        if form.is_valid():
            name = form.cleaned_data['your_name']  # Datos validados
            return HttpResponseRedirect("/thanks/")
```

## 🛡️ **Validación Implementada**

### **1. Validación Automática**
- ✅ `max_length` en CharField
- ✅ Formato de email en EmailField
- ✅ Tipos de archivo permitidos

### **2. Validación Personalizada**
```python
def clean_price(self):
    price = self.cleaned_data['price']
    if price <= 0:
        raise ValidationError("El precio debe ser mayor a cero")
    return price

def clean(self):  # Validación de múltiples campos
    cleaned_data = super().clean()
    min_price = cleaned_data.get('min_price')
    max_price = cleaned_data.get('max_price')
    
    if min_price and max_price and min_price >= max_price:
        raise ValidationError("El precio mínimo debe ser menor al máximo")
```

## 🎨 **Métodos de Renderizado de Formularios**

### **1. Renderizado Automático Completo**
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enviar</button>
</form>
```

### **2. Renderizado Manual por Campo**
```html
<form method="post">
    {% csrf_token %}
    {% for field in form %}
        <div class="form-group">
            {{ field.errors }}
            {{ field.label_tag }}
            {{ field }}
            {% if field.help_text %}
                <div class="help">{{ field.help_text }}</div>
            {% endif %}
        </div>
    {% endfor %}
    <button type="submit">Enviar</button>
</form>
```

### **3. Control Total Manual**
```html
<form method="post">
    {% csrf_token %}
    <div class="field">
        {{ form.name.errors }}
        <label for="{{ form.name.id_for_label }}">Nombre:</label>
        {{ form.name }}
    </div>
    <button type="submit">Enviar</button>
</form>
```

## 📊 **Propiedades Útiles de Formularios**

### **Estado del Formulario**
```python
form.is_bound        # True si tiene datos, False si está vacío
form.is_valid()      # True si todos los campos son válidos
form.cleaned_data    # Diccionario con datos validados y convertidos
form.errors          # Diccionario con errores de validación
```

### **Propiedades de Campos**
```html
{{ field.label }}        <!-- Etiqueta del campo -->
{{ field.help_text }}    <!-- Texto de ayuda -->
{{ field.errors }}       <!-- Errores del campo -->
{{ field.value }}        <!-- Valor actual -->
{{ field.html_name }}    <!-- Nombre HTML del campo -->
{{ field.is_hidden }}    <!-- True si es campo oculto -->
```

## 🔧 **Ejemplos Prácticos Implementados**

### **1. Formulario Básico - NameForm**
- 📍 **URL:** `/documentos/forms/name/`
- **Demuestra:** Formulario simple, bound/unbound, is_valid()

### **2. Formulario de Contacto**
- 📍 **URL:** `/documentos/forms/contact/`
- **Demuestra:** Múltiples tipos de campos, validación personalizada

### **3. Crear Vehículo (ModelForm)**
- 📍 **URL:** `/documentos/cars/create/`
- **Demuestra:** ModelForm, manejo de archivos, CRUD

### **4. Búsqueda Avanzada**
- 📍 **URL:** `/documentos/forms/search/`
- **Demuestra:** ChoiceField, validación cruzada, GET forms

### **5. Formulario Dinámico**
- 📍 **URL:** `/documentos/forms/dynamic/`
- **Demuestra:** Campos condicionales, inicialización personalizada

## 🛠️ **Características Avanzadas**

### **1. Formularios Dinámicos**
```python
def __init__(self, *args, **kwargs):
    show_advanced = kwargs.pop('show_advanced', False)
    super().__init__(*args, **kwargs)
    
    if show_advanced:
        self.fields['advanced_field'] = forms.CharField(...)
```

### **2. Manejo de Archivos**
```python
if request.method == 'POST':
    form = CarForm(request.POST, request.FILES)  # ¡request.FILES!
    if form.is_valid():
        car = form.save()
```

### **3. Protección CSRF**
```html
<form method="post">
    {% csrf_token %}  <!-- ¡Obligatorio para POST! -->
    {{ form }}
</form>
```

## 🎯 **URLs Disponibles para Probar**

| URL | Descripción | Conceptos Demostrados |
|-----|-------------|----------------------|
| `/documentos/forms/` | Índice de ejemplos | Navegación y overview |
| `/documentos/forms/name/` | NameForm básico | Form básico, bound/unbound |
| `/documentos/forms/contact/` | Formulario contacto | Múltiples campos, validación |
| `/documentos/cars/create/` | Crear vehículo | ModelForm, archivos |
| `/documentos/forms/search/` | Búsqueda avanzada | ChoiceField, validación cruzada |
| `/documentos/forms/dynamic/` | Formulario dinámico | Campos condicionales |

## 🚀 **¡Cómo Probarlo!**

1. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Visita la página principal:**
   ```
   http://127.0.0.1:8000/documentos/forms/
   ```

3. **Prueba cada ejemplo:**
   - Llena formularios correctos ✅
   - Envía formularios con errores ❌
   - Observa la validación en acción

## 💡 **Conceptos Clave Aprendidos**

1. **Form vs ModelForm:** Form para control total, ModelForm para rapidez
2. **Bound vs Unbound:** Con datos vs sin datos
3. **is_valid() y cleaned_data:** Validación y datos limpios  
4. **GET vs POST:** Mostrar vs procesar
5. **Renderizado flexible:** Automático vs manual
6. **Validación robusta:** Automática y personalizada
7. **Manejo de archivos:** ImageField y FileField
8. **Protección CSRF:** Seguridad incluida

## 📚 **Archivos Principales Creados**

```
documentos/
├── forms.py              # Definición de formularios
├── views.py              # Vistas que manejan formularios  
├── urls.py               # URLs de formularios
├── templates/documentos/forms/
│   ├── base_form.html    # Template base
│   ├── examples_index.html
│   ├── name_form.html
│   ├── contact_form.html
│   └── thanks.html
└── create_sample_data.py # Datos de ejemplo
```

¡**Tu proyecto ahora implementa completamente la documentación de formularios de Django!** 🎉