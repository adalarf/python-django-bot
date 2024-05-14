from django.urls import path
from app.internal.transport.rest.handlers import api

urlpatterns = [
    path("", api.urls),
]
