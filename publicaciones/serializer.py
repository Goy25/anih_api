from rest_framework import serializers
from .models import Publicacion, Recinto


class PublicacionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Publicacion
    fields = "__all__"


class RecintoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Recinto
    fields = "__all__"
