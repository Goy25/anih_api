from django.db import models

# Create your models here.

class Rol(models.Model):

  class Meta:
    db_table = "Rol"

  IDRol = models.AutoField(primary_key=True)
  Tipo = models.TextField(max_length=20)


class Usuario(models.Model):

  class Meta:
    db_table = "Usuario"

  IDUsuario = models.AutoField(primary_key=True)
  Apellido = models.TextField(max_length=45)
  Nombre = models.TextField(max_length=45)
  Alias = models.TextField(max_length=45, unique=True)
  Correo = models.EmailField(max_length=75, unique=True)
  Contraseña = models.TextField(max_length=100)
  FechaNacimiento = models.DateField()
  Genero = models.CharField(max_length=1)
  Intentos = models.IntegerField(default=0)
  Tipo = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, default=2, related_name="Usuarios")


  def __str__(self) -> str:
    return self.Alias

class Log(models.Model):

  class Meta:
    db_table = "Log"

  IDUsuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="Logs")
  Log = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return f"{str(self.IDUsuario)} - {self.Log}"

class Contacto(models.Model):

  class Meta:
    db_table = "Contacto"

  Telefono = models.IntegerField(primary_key=True, auto_created=False)
  Nombre = models.CharField(max_length=150)


class Tiene(models.Model):

  class Meta:
    db_table = "Tiene"

  IDUsuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="Contactos")
  Telefono = models.ForeignKey(Contacto, on_delete=models.DO_NOTHING, related_name="Vinculos")
  Relacion = models.CharField(max_length=30)