from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from registro import views

router = routers.DefaultRouter()
router.register("usuario", views.UsuarioView, "usuario")
router.register("log", views.LogView, "log")

urlpatterns = [
  path("anih/", include(router.urls)),
  path("anih/inicio-sesion/", views.VerificarUsuario.as_view(), name="inicio-sesion"),
  path("anih/obtenerCodigo/", views.CodigoConfirmacion.as_view(), name="obtenerCodigo"),
  path("anih/existe-contacto/", views.RevisarContactos.as_view(), name="existe-contacto"),
  path("anih/guardar-contactos/", views.GuardarContactos.as_view(), name="guardar-contactos"),
  path("anih/contactos/", views.ContactosUsuario.as_view(), name="contactos"),
  path("anih/actualizar-user/", views.ActualizarUsuario.as_view(), name="actualizar-user"),
  path("anih/actualizar-contacto/", views.ActualizarContacto.as_view(), name="actualizar-contacto"),
  path("anih/agregar-contacto/", views.AgregarContacto.as_view(), name="agregar-contacto"),
  path("anih/eliminar-contacto/", views.EliminarContacto.as_view(), name="eliminar-contacto"),
  path("docs/", include_docs_urls(title="Registro de Usuarios"))
]
