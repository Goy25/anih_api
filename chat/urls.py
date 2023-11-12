from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from chat import views

router = routers.DefaultRouter()
router.register("preguntas", views.PreguntaView, "preguntas")

urlpatterns = [
  path("anih/", include(router.urls)),
  path("anih/chat-bot/", views.MesajeChatBot.as_view(), name="chat-bot"),
  path("docs/", include_docs_urls(title="Mensajes"))
]