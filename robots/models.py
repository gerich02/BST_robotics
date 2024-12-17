from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    RegexValidator)
from django.db import models

from .constants import (ERROR_MODEL_FORMAT, ERROR_SERIAL_FORMAT,
                        ERROR_VERSION_FORMAT, MODEL_LENGTH, ROBOT_MODEL_REGEX,
                        ROBOT_SERIAL_REGEX, ROBOT_VERSION_REGEX,
                        VERSION_MAX_LENGTH, VERSION_MIN_LENGTH)


class Robot(models.Model):
    """
    Модель Robot представляет информацию о роботе.

    Атрибуты:
        serial (CharField): Уникальный серийный номер робота, состоящий из
            модели и версии, разделённых дефисом. Например, "AB-12".
        model (CharField): Код модели робота, состоящий из двух символов
            (букв или цифр).
        version (CharField): Версия робота, состоящая из одного или двух
            символов (букв или цифр).
        created (DateTimeField): Дата и время создания записи о роботе.
            Не может быть пустым или null.

    Методы:
        save: Переопределённый метод сохранения, который вызывает
            full_clean() перед сохранением, чтобы обеспечить валидацию
            всех данных модели.
    """

    serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=ROBOT_SERIAL_REGEX,
                message=ERROR_SERIAL_FORMAT,
            )
        ],
    )
    model = models.CharField(
        max_length=MODEL_LENGTH,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=ROBOT_MODEL_REGEX,
                message=ERROR_MODEL_FORMAT,
            ),
            MinLengthValidator(MODEL_LENGTH),
            MaxLengthValidator(MODEL_LENGTH),
        ],
    )
    version = models.CharField(
        max_length=VERSION_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=ROBOT_VERSION_REGEX,
                message=ERROR_VERSION_FORMAT,
            ),
            MinLengthValidator(VERSION_MIN_LENGTH),
            MaxLengthValidator(VERSION_MAX_LENGTH),
        ],
    )
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
