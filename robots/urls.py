from django.urls import path

from .views import ExportToExcelView, RobotCreateView

urlpatterns = [
    path("create/", RobotCreateView.as_view(), name="robot-create"),
    path("export_to_excel/", ExportToExcelView.as_view(), name="export_to_excel"),
]
