from django.db import models
from registro.models import Usuario

# Create your models here.

class Publicacion(models.Model):

  class Meta:
    db_table = "Publicacion"

  IDPublicacion = models.AutoField(primary_key=True)
  Titulo = models.CharField(max_length=200)
  FechaPublicacion = models.DateField(auto_now_add=True)
  Contenido = models.CharField(max_length=5000)
  FechaNoticia = models.DateField()
  Imagen = models.CharField(max_length=500)

  def __str__(self) -> str:
    return f"{self.Titulo}"


class Recinto(models.Model):

  class Meta:
    db_table = "Recinto"
  
  IDRecinto = models.AutoField(primary_key=True)
  Nombre = models.CharField(max_length=100)
  Direccion = models.CharField(max_length=150)
  Telefono = models.PositiveIntegerField(null=True)
  Horario = models.CharField(max_length=45)
  Imagen = models.CharField(max_length=500)