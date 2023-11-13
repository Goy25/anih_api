from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UsuarioSerializer, ContactoSerializer, LogSerializer, RolSerializer, TieneSerializer
from .models import Usuario, Log, Contacto, Tiene, Rol
import random
import string
import smtplib
from email.mime.text import MIMEText

# Create your views here.

class UsuarioView(viewsets.ModelViewSet):
  serializer_class = UsuarioSerializer
  queryset = Usuario.objects.all()

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    hashed_password = make_password(validated_data['Contraseña'])
    data_to_save = {**validated_data, 'Contraseña': hashed_password}
    usuario = Usuario.objects.create(**data_to_save)
    serializer = self.get_serializer(usuario)
    print(serializer.data)
    return Response({"id": serializer.data["IDUsuario"]}, status=status.HTTP_201_CREATED)


class LogView(viewsets.ModelViewSet):
  serializer_class = LogSerializer
  queryset = Log.objects.all()


class RolView(viewsets.ModelViewSet):
  serializer_class = RolSerializer
  queryset = Rol.objects.all()


class ContactoView(viewsets.ModelViewSet):
  serializer_class = ContactoSerializer
  queryset = Contacto.objects.all()


class TieneView(viewsets.ModelViewSet):
  serializer_class = TieneSerializer
  queryset = Tiene.objects.all()


class ActualizarUsuario(APIView):

  def put(self, request, format=None):
    datos = request.data
    usuario = Usuario.objects.get(IDUsuario=datos["Id"])
    if datos["Password"] != "":
      setattr(usuario, "Contraseña", make_password(datos["Password"]))
    setattr(usuario, "Nombre", datos["Nombre"])
    setattr(usuario, "Apellido", datos["Apellido"])
    if (datos["Alias"] != usuario.Alias):
      try:
        Usuario.objects.get(Alias=datos["Alias"])
        return Response({'mensaje': 'AE'}, status=status.HTTP_200_OK)
      except Exception as e:
        setattr(usuario, "Alias", datos["Alias"])
    setattr(usuario, "FechaNacimiento", datos["FechaNacimiento"])
    setattr(usuario, "Genero", datos["Genero"])
    usuario.save()
    return Response({'mensaje': 'ok'}, status=status.HTTP_200_OK)


class ActualizarContacto(APIView):

  def put(self, request, format=None):
    datos = request.data
    tiene = Tiene.objects.get(IDUsuario=datos["Id"], Telefono=datos["Telefono"])
    if datos["Relacion"] != tiene.Relacion:
      setattr(tiene, "Relacion", datos["Relacion"])
      return Response({'mensaje': 'ok'}, status=status.HTTP_200_OK)
    return Response({"mensaje": "Sin cambios"}, status=status.HTTP_200_OK)
  

class AgregarContacto(APIView):

  def post(self, request, format=None):
    datos = request.data
    usuario = Usuario.objects.get(IDUsuario=datos["Id"])
    print("--1--")
    try:
      contacto = Contacto.objects.get(Telefono=datos["Telefono"])
      print("--2--")
      try:
        print("--5--")
        tiene = Tiene.objects.get(IDUsuario=usuario, Telefono=contacto)
        print("--6--")
        return Response({'mensaje': 'AE'}, status=status.HTTP_200_OK)
      except Exception as e:
        print("--7--")
        Tiene.objects.create(IDUsuario=datos["Id"], Telefono=contacto, Relacion=datos["Relacion"])
        print("--8--")
        return Response({'mensaje': 'RC'}, status=status.HTTP_200_OK)
    except Exception as e:
      Contacto.objects.create(Telefono=datos["Telefono"], Nombre=datos["Nombre"])
      Tiene.objects.create(IDUsuario=usuario, Telefono=Contacto.objects.get(Telefono=datos["Telefono"]), Relacion=datos["Relacion"])
      return Response({'mensaje': 'CC'}, status=status.HTTP_200_OK)


class EliminarContacto(APIView):

  def put(self, request, format=None):
    datos = request.data
    tiene = Tiene.objects.get(IDUsuario=datos["Id"], Telefono=datos["Telefono"])
    tiene.delete()
    return Response({'mensaje': 'ok'}, status=status.HTTP_200_OK)


class VerificarUsuario(APIView):
  def post(self, request, format=None):
    print(make_password("Adri@n25"))
    correo = request.data.get('Correo')
    contraseña = request.data.get('Contraseña')
    try:
      usuario = Usuario.objects.get(Correo=correo)
      if check_password(contraseña, usuario.Contraseña):
        usuario.Intentos = 0
        usuario.save()
        serializer = UsuarioSerializer(usuario)
        Log.objects.create(IDUsuario=usuario)
        return Response({"Alias": serializer.data["Alias"], "IDUsuario": serializer.data["IDUsuario"], "Tipo": usuario.Tipo.Tipo}, status=status.HTTP_200_OK)
      else:
        usuario.Intentos += 1
        usuario.save()
        if usuario.Intentos >= 3:
          try:
            new_pass = generar_pass()
            enviar_correo(usuario.Correo, 'Nueva Contraseña Anih', 'Se reestablecio su contaseña.\nLa nueva contraseña es: ' + new_pass)
            usuario.Intentos = 0
            usuario.Contraseña = make_password(new_pass)
            usuario.save()
          except Exception:
            return Response({'mensaje': 'CR'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'mensaje': 'CI'}, status=status.HTTP_401_UNAUTHORIZED)
    except Usuario.DoesNotExist:
      return Response({'mensaje': 'UNE'}, status=status.HTTP_401_UNAUTHORIZED)


class CodigoConfirmacion(APIView):
  def post(self, request, format=None):
    correo = request.data.get('Correo')
    codVerificacion = random.randint(100000, 999999)
    enviar_correo(correo, "Codigo Confirmacion", f'Su código de confirmación es: {codVerificacion}')
    return Response({'codigo': codVerificacion}, status=status.HTTP_200_OK)


class GuardarContactos(APIView):

  def post(self, request, format=None):
    id_usuario = Usuario.objects.get(IDUsuario=request.data.get('id'))
    contactos = request.data.get('contactos')
    for contacto in contactos:
      print(contacto)
      try:
        cont = Contacto.objects.get(Telefono=contacto["Numero"])
      except Exception:
        print("No existe")
        cont = Contacto.objects.create(Nombre=contacto["Nombre"], Telefono=contacto["Numero"])
      finally:
        Tiene.objects.create(IDUsuario=id_usuario, Telefono=cont, Relacion=contacto["Relacion"])
    return Response({**request.data, 'mensaje': "ok"}, status=status.HTTP_200_OK)


class RevisarContactos(APIView):

  def post(self, request, format=None):
    try:
      contacto = Contacto.objects.get(Telefono=request.data.get('Numero'))
      serializer = ContactoSerializer(contacto)
      return Response({'mensaje': 'Existe', 'Nombre': serializer.data['Nombre']}, status=status.HTTP_200_OK)
    except Contacto.DoesNotExist:
      return Response({'mensaje': 'No existe'}, status=status.HTTP_200_OK)


class ContactosUsuario(APIView):

  def post(self, request, format=None):
    try:
      usuario = Usuario.objects.get(IDUsuario=request.data.get('id'))
      contactos = Tiene.objects.filter(IDUsuario=usuario.IDUsuario)
      # serializer = ContactoSerializer([contacto.Telefono for contacto in contactos], many=True)
      return Response([{"Numero": contacto.Telefono.Telefono, "Nombre": contacto.Telefono.Nombre, "Relacion": contacto.Relacion} for contacto in contactos], status=status.HTTP_200_OK)
    except Exception as e:
      return Response({'mensaje': 'No existe'}, status=status.HTTP_200_OK)


def enviar_correo(correo, asunto, mensaje):
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  sender_email = "anih.contactar@gmail.com"
  sender_password = "aqexkafufyjqwgwx"
  msg = MIMEText(mensaje)
  msg['Subject'] = asunto
  msg['From'] = sender_email
  msg['To'] = correo
  try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [correo], msg.as_string())
    server.quit()
  except Exception as e:
    print(f'Error al enviar el correo: {str(e)}')


def generar_pass(longitud = 16):
  caracteres = string.ascii_letters + string.digits + string.punctuation
  contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
  return contrasena
