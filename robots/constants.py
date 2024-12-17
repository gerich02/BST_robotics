ROBOT_SERIAL_REGEX = r"^[A-Za-z0-9]{2}-[A-Za-z0-9]{1,2}$"
ROBOT_MODEL_REGEX = r"^[A-Za-z0-9]{2}$"
ROBOT_VERSION_REGEX = r"^[A-Za-z0-9]{1,2}$"
ERROR_SERIAL_FORMAT = (
    "Serial должен быть в формате 'model-version', где 'model' это 2 буквы "
    "или цифры, а 'version' это 1 или 2 цифры."
)
ERROR_MODEL_FORMAT = (
    "Модель должна быть двух-символьной последовательностью "
    "из букв или цифр."
)
ERROR_VERSION_FORMAT = (
    "Версия должна быть одно/двух-символьной последовательностью "
    "из букв или цифр."
)
MODEL_LENGTH = 2
VERSION_MIN_LENGTH = 1
VERSION_MAX_LENGTH = 2
ERROR_FUTURE_DATE = "Дата не может быть в будущем."
ERROR_INVALID_DATA = "Invalid data"
ERROR_INVALID_JSON = "Invalid JSON"
ERROR_FUTURE_DATE = "Дата не может быть в будущем."
