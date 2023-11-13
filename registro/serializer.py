from rest_framework import serializers
from .models import Usuario, Log, Contacto, Tiene, Rol

class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Log
    fields = "__all__"


class ContactoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contacto
    fields = "__all__"


class TieneSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tiene
    fields = "__all__"

class RolSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rol
    fields = "__all__"