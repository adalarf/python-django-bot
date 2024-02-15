from django.urls import path
from app.internal.transport.rest.handlers import GetUserInfoView

urlpatterns = [
    path("me/<int:id>/", GetUserInfoView.as_view()),
]
