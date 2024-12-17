import json

from django.test import TestCase
from django.urls import reverse

from robots.constants import ERROR_FUTURE_DATE, ERROR_INVALID_DATA
from robots.models import Robot


class RobotCreateViewTest(TestCase):
    """Тесты для проверки работы представления создания робота."""

    def setUp(self):
        """Предустановка URL для создания робота."""
        self.url = reverse("robot-create")

    def test_create_robot_success(self):
        """
        Проверяет успешное создание робота с валидными данными.

        Убеждается, что:
        - Ответ имеет статус 201.
        - Возвращается сообщение "Robot created".
        - Робот корректно сохраняется в базе данных.
        """
        data = {"model": "AB", "version": "01", "created": "2024-12-16 10:00:00"}
        response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Robot created"})
        robot = Robot.objects.get(serial="AB-01")
        self.assertEqual(robot.model, "AB")
        self.assertEqual(robot.version, "01")
        self.assertEqual(str(robot.created), "2024-12-16 10:00:00+00:00")

    def test_create_robot_missing_field(self):
        """
        Проверяет поведение при отсутствии обязательного поля.

        Убеждается, что:
        - Ответ имеет статус 400.
        - Возвращается ошибка с текстом ERROR_INVALID_DATA.
        """
        data = {"model": "AB", "version": "01"}
        response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": ERROR_INVALID_DATA})

    def test_create_robot_invalid_json(self):
        """
        Проверяет обработку некорректного JSON.

        Убеждается, что:
        - Ответ имеет статус 400.
        - Возвращается ошибка с текстом ERROR_INVALID_DATA.
        """
        invalid_data = '{ "model": "AB", "version": "01" }'
        response = self.client.post(
            self.url, invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": ERROR_INVALID_DATA})

    def test_create_robot_invalid_date(self):
        """
        Проверяет поведение при использовании даты из будущего.

        Убеждается, что:
        - Ответ имеет статус 400.
        - Возвращается ошибка с текстом ERROR_FUTURE_DATE.
        """
        data = {"model": "AB", "version": "01", "created": "2026-12-16 10:00:00"}
        response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": ERROR_FUTURE_DATE})

    def test_create_robot_invalid_serial(self):
        """
        Проверяет обработку некорректного серийного номера.

        Убеждается, что:
        - Ответ имеет статус 400.
        - Возвращается ошибка валидации серийного номера.
        """
        response = self.client.post(
            "/robots/create/",
            data=json.dumps(
                {
                    "serial": "invalid-serial",
                    "model": "AB",
                    "version": "12",
                    "created": "2023-01-01T12:00:00Z",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
