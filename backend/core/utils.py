import random
import string

from rest_framework.response import Response
from rest_framework.views import exception_handler


DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(size: int, chars=DEFAULT_CHAR_STRING):
    return ''.join(random.choice(chars) for _ in range(size))


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response({'errors': {'body': ['Internal server error']}}, status=500)
    return response
