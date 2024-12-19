import json
from django.http import JsonResponse
from django.views import View
from customers.models import Customer
from orders.models import Order


class OrderCreateView(View):
    """
    Представление для создания нового заказа.

    Обрабатывает POST-запросы для создания заказа
    и серийного номера робота. Если клиент с такой почтой не существует, он
    будет создан автоматически.
    """

    def post(self, request, *args, **kwargs):
        """
        Создаёт новый заказ на робота для клиента.

        Принимает следующие данные:
            - customer_email (str): Почта клиента.
            - robot_serial (str): Серийный номер робота.

        Возвращает:
            - 201: Если заказ успешно создан.
            - 400: В случае ошибок в данных.
        """
        try:
            data = json.loads(request.body)
            customer_email = data.get("customer_email")
            robot_serial = data.get("robot_serial")
            if not customer_email or not robot_serial:
                return JsonResponse(
                    {"error": "Both email and serial are required."},
                    status=400
                )
            customer, created = Customer.objects.get_or_create(
                email=customer_email
            )
            Order.objects.create(
                customer=customer,
                robot_serial=robot_serial
            )

            return JsonResponse(
                {"message": "Order created successfully."},
                status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
