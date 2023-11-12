from django.db import models
from registro.models import Usuario


# Create your models here.

class Pregunta(models.Model):

  class Meta:
    db_table = "Pregunta"
  
  IDPregunta = models.AutoField(primary_key=True)
  Pregunta = models.CharField(max_length=1000)
  Respuesta = models.CharField(max_length=5000)
  IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="Preguntas")