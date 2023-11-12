from django.db import models
from registro.models import Usuario

# Create your models here.

class Categoria(models.Model):

  class Meta:
    db_table = 'Categoria'

  IDCategoria = models.AutoField(primary_key=True)
  Nombre = models.CharField(max_length=50)

  def __str__(self):
    return self.Nombre


class Ocupacion(models.Model):

  class Meta:
    db_table = 'Ocupacion'

  Nombre = models.CharField(max_length=50)

  def __str__(self):
    return self.Nombre


class Denuncia(models.Model):

  class Meta:
    db_table = 'Denuncia'

  IDDenuncia = models.AutoField(primary_key=True)
  FechaHecho = models.DateTimeField()
  Lugar = models.CharField(max_length=150)
  Frecuencia = models.CharField(max_length=100)
  Descripcion = models.CharField(max_length=5000)
  FechaDenuncia = models.DateTimeField(auto_now_add=True)
  IDDenunciante = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="Denuncias")


class Evidencia(models.Model):

  class Meta:
    db_table = 'Evidencia'

  IDEvidencia = models.AutoField(primary_key=True)
  archivo = models.FileField(upload_to='evidencias/')
  IDDenuncia = models.ForeignKey(Denuncia, on_delete=models.DO_NOTHING, related_name="Evidencias")


class TieneDC(models.Model):

  class Meta:
    db_table = "TieneDC"
  
  IDDenuncia = models.ForeignKey(Denuncia, on_delete=models.DO_NOTHING, related_name="Categorias")
  IDCategoria =models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, related_name="Denuncias")


class Actor(models.Model):

  class Meta:
    db_table = 'Actor'

  IDActor = models.AutoField(primary_key=True)
  CI = models.IntegerField()
  Nombre = models.CharField(max_length=75)
  Apellido = models.CharField(max_length=75)
  FechaNacimiento = models.DateField()
  Telefono = models.IntegerField()
  Direccion = models.CharField(max_length=150)
  Zona = models.CharField(max_length=50, blank=True)
  Nacionalidad = models.CharField(max_length=50)
  EstadoCivil = models.CharField(max_length=30)
  Sexo = models.CharField(max_length=1)
  Ocupacion = models.CharField(max_length=30)


  def __str__(self):
    return f"{self.Nombre} {self.Apellido}"


class Agresor(models.Model):

  class Meta:
    db_table = 'Agresor'
  
  IDActor = models.OneToOneField(Actor, on_delete=models.DO_NOTHING, related_name="Agresor")
  Descripcion = models.CharField(max_length=500)
  RelacionVictima = models.CharField(max_length=50)

  def __str__(self):
    return str(self.IDActor)


class Testigo(models.Model):

  class Meta:
    db_table = 'Testigo'

  IDActor = models.OneToOneField(Actor, on_delete=models.DO_NOTHING, related_name="Testigo")
  Testimonio = models.CharField(max_length=5000)

  def __str__(self):
    return str(self.IDActor)


class Victima(models.Model):

  class Meta:
    db_table = 'Victima'
  
  IDActor = models.OneToOneField(Actor, on_delete=models.DO_NOTHING, related_name="Victima")
  Departamento = models.CharField(max_length=30)
  Zona = models.CharField(max_length=30)
  Ingresos = models.CharField(max_length=30)
  AsistenciaMedica = models.CharField(max_length=2)
  NivelEducativo = models.CharField(max_length=30)


class Implica(models.Model):

  class Meta:
    db_table = 'Implica'
  
  IDDenuncia = models.ForeignKey(Denuncia, on_delete=models.DO_NOTHING, related_name="Actores")
  IDActor = models.ForeignKey(Actor, on_delete=models.DO_NOTHING, related_name="Denuncias")
