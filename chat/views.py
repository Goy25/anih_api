from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Pregunta
from .serializer import PreguntaSerializer
from rest_framework.response import Response
from rest_framework import status
from registro.models import Usuario
import chat.anih_gpt as bot

# Create your views here.

class PreguntaView(viewsets.ModelViewSet):
  serializer_class = PreguntaSerializer
  queryset = Pregunta.objects.all()


class MesajeChatBot(APIView):

  def post(self, request, format=None):
    try:
      usuario = Usuario.objects.get(IDUsuario=request.data.get('IDEmisor'))
      mensaje = request.data.get('Contenido')
      respuesta = bot.mandar_mensaje(mensaje)
      Pregunta.objects.create(Pregunta=mensaje, Respuesta=respuesta, IDUsuario=usuario)
      return Response({'Respuesta': respuesta}, status=status.HTTP_200_OK)
    except Exception as e:
      print("Error:", e)
      return Response({'IDEmisor': 0, 'Contenido': 'Hubo un error'}, status=status.HTTP_200_OK)