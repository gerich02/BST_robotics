import json
from datetime import datetime

from django.http import JsonResponse
from django.utils.timezone import make_aware, now
from django.views import View
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
