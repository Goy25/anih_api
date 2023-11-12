from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from denuncia import views


router = routers.DefaultRouter()
router.register("categoria", views.CategoriaView, "categoria")
router.register("denuncia", views.DenunciaView, "denuncia")
router.register("actor", views.ActorView, "actor")
router.register("agresor", views.AgresorView, "agresor")
router.register("testigo", views.TestigoView, "testigo")
router.register("victima", views.VictimaView, "victima")
router.register("tieneDC", views.TieneDCView, "tieneDC")

urlpatterns = [
  path("anih/", include(router.urls)),
  path("anih/denunciar/", views.Denunciar.as_view(), name="denunciar"),
  path("anih/buscar/", views.BuscarDenuncia.as_view(), name="buscar"),

]