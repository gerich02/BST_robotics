from django.urls import path

from .views import RobotCreateView

urlpatterns = [
    path("create/", RobotCreateView.as_view(), name="robot-create"),
]
