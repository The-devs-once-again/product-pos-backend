import random
import string
from typing import Type
from django.db import models


class StringUtils:
    @staticmethod
    def generate_random_string(string_length: int):
        characters = string.ascii_letters + string.digits
        result = ''.join(random.choice(characters) for _ in range(string_length))
        return result.upper()


class DatetimeUtils:
    @staticmethod
    def format_datatime(datetime_field):
        return datetime_field.strftime('%Y-%m-%d %H:%M:%S')


class RequestsUtils:
    @staticmethod
    def get_query_params(lookup_id: str, lookup_value):
        return {lookup_id: lookup_value}


class ModelUtils:
    @staticmethod
    def get_model_instance(model: Type[models.Model], validated_data: any) -> any:
        return model.objects.create(**validated_data)
