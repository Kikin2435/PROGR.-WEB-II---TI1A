from django.db import models

class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios')

    def __str__(self):
        return self.nombre
