import json
from datetime import datetime

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import make_aware, now
from django.views import View
from openpyxl import Workbook

from robots.constants import (ERROR_FUTURE_DATE, ERROR_INVALID_DATA,
                              ERROR_INVALID_JSON)
from robots.models import Robot


class RobotCreateView(View):
    """
    Представление для создания нового робота.

    Обрабатывает POST-запросы для создания робота в базе данных. Ожидает
    данные в формате JSON с полями "model", "version" и "created". В случае
    ошибок возвращает соответствующие сообщения об ошибке.

    Методы:
        post: Создаёт нового робота и сохраняет его в базе данных.
    """

    def post(self, request, *args, **kwargs):
        """
        Создаёт нового робота.

        Принимает следующие данные:
            - model (str): Модель робота.
            - version (str): Версия робота.
            - created (str): Дата и время создания робота (ISO 8601).

        Возвращает:
            - 201: Если робот успешно создан.
            - 400: В случае ошибок в данных.
        """
        try:
            data = json.loads(request.body)
            model = data.get("model")
            version = data.get("version")
            created_str = data.get("created")
            if not model or not version or not created_str:
                return JsonResponse({"error": ERROR_INVALID_DATA}, status=400)

            try:
                created = make_aware(datetime.fromisoformat(created_str))
                if created > now():
                    return JsonResponse(
                        {"error": ERROR_FUTURE_DATE},
                        status=400
                    )
            except ValueError:
                return JsonResponse({"error": ERROR_INVALID_DATA}, status=400)

            serial = f"{model}-{version}"
            robot = Robot(
                serial=serial,
                model=model,
                version=version,
                created=created
            )
            robot.save()
            return JsonResponse({"message": "Robot created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": ERROR_INVALID_JSON}, status=400)


class ExportToExcelView(View):
    """
    Представление для экспорта данных о роботах в Excel файл.

    Обрабатывает GET-запросы для создания Excel файла с данными о роботах.
    Для каждой модели робота создаётся отдельный лист в файле, где указаны
    её версия и количество роботов. В случае успешного выполнения возвращает
    файл с расширением .xlsx.

    Методы:
        get: Генерирует и отправляет файл Excel с данными о роботах.
    """

    def get(self, request, *args, **kwargs):
        """
        Экспортирует данные о роботах в Excel файл.

        Принимает запрос и генерирует Excel файл с несколькими листами.
        Каждый лист содержит информацию о роботах для одной модели,
        сгруппированную по версиям. В каждом листе указаны следующие данные:
            - Model (str): Модель робота.
            - Version (str): Версия робота.
            - Count (int): Количество роботов данной модели и версии.

        Возвращает:
            - 200: Если файл успешно создан и отправлен для скачивания.
            - 500: В случае ошибки при генерации файла.
        """
        robots = Robot.objects.values(
            "model",
            "version"
        ).annotate(count=Count("id"))
        wb = Workbook()
        models = set(robot["model"] for robot in robots)
        for model in models:
            ws = wb.create_sheet(title=model)
            ws.append(["Model", "Version", "Count"])
            model_robots = [
                robot for robot in robots if robot["model"] == model
            ]
            for robot in model_robots:
                ws.append([robot["model"], robot["version"], robot["count"]])
        wb.remove(wb["Sheet"])
        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = "attachment; filename=robots_rp.xlsx"
        wb.save(response)
        return response
