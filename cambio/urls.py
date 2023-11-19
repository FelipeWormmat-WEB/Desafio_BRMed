from django.urls import path

from .views import ConsultaMoeda

app_name = "cambio"


urlpatterns = [path("", ConsultaMoeda.as_view(), name="index")]
