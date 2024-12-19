from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from .models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def post_save_customer_notification(instance, created, **kwargs):
    """
    Обработчик сигнала, который отправляет уведомление клиенту, когда робот
    становится доступен в наличии.

    Параметры:
        sender (Model): Модель, от которой был сгенерирован сигнал.
        instance (Robot): Экземпляр модели Robot.
        created (bool): Флаг, указывающий на создание нового объекта.

    Действия:
        - Отправляет уведомление клиенту, сделавшему первый заказ на робота.
        - Удаляет первый заказ с данным серийным номером.
    """
    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)
        if orders.exists():
            oldest_order = orders.order_by('id').first()
            customer_email = oldest_order.customer.email
            subject = "Робот теперь в наличии"
            message = (
                f"Добрый день!\n"
                f"Недавно вы интересовались нашим роботом модели  "
                f"{instance.model}, версии {instance.version}.\n"
                "Этот робот теперь в наличии. Если вам подходит "
                "этот вариант - пожалуйста, свяжитесь с нами."
            )
            send_mail(
                subject,
                message,
                'no-reply@example.com',
                [customer_email],
                fail_silently=False,
            )
            oldest_order.delete()
