from .models import Categoria, Denuncia, Actor, Agresor, Testigo, Victima, Implica, TieneDC
from .serializer import CategoriaSerializer, DenunciaSerializer, ActorSerializer, AgresorSerializer, TestigoSerializer, VictimaSerializer, TieneDCSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from registro.models import Usuario
from datetime import datetime

# Create your views here.


class CategoriaView(viewsets.ModelViewSet):
  serializer_class = CategoriaSerializer
  queryset = Categoria.objects.all()


class DenunciaView(viewsets.ModelViewSet):
  serializer_class = DenunciaSerializer
  queryset = Denuncia.objects.all()


class ActorView(viewsets.ModelViewSet):
  serializer_class = ActorSerializer
  queryset = Actor.objects.all()


class AgresorView(viewsets.ModelViewSet):
  serializer_class = AgresorSerializer
  queryset = Agresor.objects.all()


class TestigoView(viewsets.ModelViewSet):
  serializer_class = TestigoSerializer
  queryset = Testigo.objects.all()


class VictimaView(viewsets.ModelViewSet):
  serializer_class = VictimaSerializer
  queryset = Victima.objects.all()


class TieneDCView(viewsets.ModelViewSet):
  serializer_class = TieneDCSerializer
  queryset = TieneDC.objects.all()


class Denunciar(APIView):

  def post(self, request, format=None):
    try:
      usuario = Usuario.objects.get(IDUsuario=request.data.get('id'))
      datos_denuncia = request.data
      print(datos_denuncia)
      fecha_hecho_str = datos_denuncia.get('FechaHecho') + ' ' + datos_denuncia.get('HoraHecho')
      fecha_hecho = datetime.strptime(fecha_hecho_str, '%Y-%m-%d %H:%M')
      denuncia = Denuncia.objects.create(FechaHecho=fecha_hecho,
                                         Lugar=datos_denuncia.get('Lugar'),
                                         Frecuencia=datos_denuncia.get('Frecuencia'),
                                         Descripcion=datos_denuncia.get('Descripcion'),
                                         IDDenunciante=usuario)
      cat = Categoria.objects.get(Nombre=datos_denuncia.get("Tipo"))
      TieneDC.objects.create(IDDenuncia=denuncia, IDCategoria=cat)
      for victima in request.data.get('victima', []):
        actor = Actor.objects.create(CI=int(victima.get('CI')),
                                     Nombre=victima.get('Nombre'),
                                     Apellido=victima.get('Apellido'),
                                     FechaNacimiento=victima.get('FechaNacimiento'),
                                     Telefono=int(victima.get('Telefono')),
                                     Direccion=victima.get('Direccion'),
                                     Nacionalidad=victima.get('Nacionalidad'),
                                     Zona=victima.get('Zona'),
                                     EstadoCivil=victima.get('EC'),
                                     Sexo=victima.get('Genero'),
                                     Ocupacion=victima.get('Ocupacion'))
        Implica.objects.create(IDDenuncia=denuncia, IDActor=actor)
        Victima.objects.create(IDActor=actor,
                               Departamento=victima.get('Departamento'),
                               Zona=victima.get('Zona'),
                               Ingresos=victima.get('Ingresos'),
                               AsistenciaMedica = victima.get('AsistenciaMedica'),
                               NivelEducativo = victima.get('NivelEducativo'))
      for agresor in request.data.get('agresor', []):
        actor = Actor.objects.create(CI=int(agresor.get('CI')),
                                     Nombre=agresor.get('Nombre'),
                                     Apellido=agresor.get('Apellido'),
                                     FechaNacimiento=agresor.get('FechaNacimiento'),
                                     Telefono=int(agresor.get('Telefono')),
                                     Direccion=agresor.get('Direccion'),
                                     Nacionalidad=agresor.get('Nacionalidad'),
                                     EstadoCivil=agresor.get('EC'),
                                     Sexo=agresor.get('Genero'),
                                     Ocupacion=agresor.get('Ocupacion'))
        Implica.objects.create(IDDenuncia=denuncia, IDActor=actor)
        Agresor.objects.create(IDActor=actor,
                               Descripcion=agresor.get('Descripcion'),
                               RelacionVictima=agresor.get('RelacionVictima'))
      for testigo in request.data.get('testigo', []):
        actor = Actor.objects.create(CI=int(testigo.get('CI')),
                                     Nombre=testigo.get('Nombre'),
                                     Apellido=testigo.get('Apellido'),
                                     FechaNacimiento=testigo.get('FechaNacimiento'),
                                     Telefono=int(testigo.get('Telefono')),
                                     Direccion=testigo.get('Direccion'),
                                     Nacionalidad=testigo.get('Nacionalidad'),
                                     Zona=testigo.get('Zona'),
                                     EstadoCivil=testigo.get('EC'),
                                     Sexo=testigo.get('Genro'),
                                     Ocupacion=testigo.get('Ocupacion'))
        Implica.objects.create(IDDenuncia=denuncia, IDActor=actor)
        Testigo.objects.create(IDActor=actor, Testimonio=testigo.get('Testimonio'))
      return Response({'mensaje': 'Denuncia creada'}, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({'mensaje': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BuscarDenuncia(APIView):

  def post(self, request, format=None):
    try:
      datos = request.data
      denuncias = Denuncia.objects.filter(FechaHecho__gte=datos.get('FechaDesde'),
                                          FechaHecho__lte=datos.get('FechaHasta'),
                                          Lugar__icontains=datos.get('Lugar'))
      denuncias = DenunciaSerializer(denuncias, many=True)
      return Response(denuncias.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({'mensaje': str(e)}, status=status.HTTP_400_BAD_REQUEST)