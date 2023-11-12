from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from publicaciones import views

router = routers.DefaultRouter()
router.register("publicacion", views.PublicacionView, "publicacion")
router.register("recinto", views.RecintoView, "recinto")

urlpatterns = [
  path("anih/", include(router.urls)),
  path("anih/estadisticaDenuncias/", views.DenunciasXCategoria.as_view(), name="estadisticaDenuncias"),
  path("anih/cantidadLogs/", views.CantidadLogs.as_view(), name="cantidadLogs"),
  path("docs/", include_docs_urls(title="Publicaciones"))
]