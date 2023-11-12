from rest_framework import serializers
from .models import Categoria, Denuncia, Actor, Agresor, Testigo, Victima, TieneDC


class CategoriaSerializer(serializers.ModelSerializer):

  class Meta:
    model = Categoria
    fields = "__all__"


class DenunciaSerializer(serializers.ModelSerializer):

  class Meta:
    model = Denuncia
    fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):

  class Meta:
    model = Actor
    fields = "__all__"


class AgresorSerializer(serializers.ModelSerializer):

  class Meta:
    model = Agresor
    fields = "__all__"


class TestigoSerializer(serializers.ModelSerializer):

  class Meta:
    model = Testigo
    fields = "__all__"


class VictimaSerializer(serializers.ModelSerializer):

  class Meta:
    model = Victima
    fields = "__all__"


class TieneDCSerializer(serializers.ModelSerializer):

  class Meta:
    model = TieneDC
    fields = "__all__"