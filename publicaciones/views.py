from .models import Publicacion, Recinto
from .serializer import PublicacionSerializer, RecintoSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from denuncia.models import Categoria
from registro.models import Log

# Create your views here.


class PublicacionView(viewsets.ModelViewSet):
  serializer_class = PublicacionSerializer
  queryset = Publicacion.objects.all()


class RecintoView(viewsets.ModelViewSet):
  serializer_class = RecintoSerializer
  queryset = Recinto.objects.all()


class DenunciasXCategoria(APIView):

  def get(self, request):
    queryset = Categoria.objects.annotate(
        count_Denuncias=Count('Denuncias')
    ).values('Nombre', 'count_Denuncias')
    data = {"labels": [i["Nombre"] for i in queryset]}
    data["datasets"] = [{"label": "Denuncias por categoria", "data": [i["count_Denuncias"] for i in queryset]}]
    return Response(data, status=status.HTTP_200_OK)


class CantidadLogs(APIView):

  def get(self, request):
    # Obtener la fecha y hora actual
    now = timezone.now()

    logs_dia = Log.objects.filter(Log__gte=now - timedelta(hours=24), Log__lte=now)

    logs_semana = Log.objects.filter(Log__gte=now - timedelta(days=7), Log__lte=now)

    logs_mes = Log.objects.filter(Log__gte=now - timedelta(days=30), Log__lte=now)

    logs_anio = Log.objects.filter(Log__gte=now - timedelta(days=365), Log__lte=now)

    return Response({
      "labels": ["Últimas 24 horas", "Última semana", "Último mes", "Último año"],
      "datasets": [
        {
          "label": "Cantidad de logs",
          "data": [logs_dia.count(), logs_semana.count(), logs_mes.count(), logs_anio.count()]
        }
      ]
    }, status=status.HTTP_200_OK)