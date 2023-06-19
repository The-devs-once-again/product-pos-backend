from dataclasses import dataclass
from typing import Optional, Type

from django.db import models
from rest_framework import serializers


@dataclass
class ViewConfig:
    serializer_class: Type[serializers.ModelSerializer]
    model: Type[models.Model]
    response_name: Optional[str] = None
    delete_message: Optional[str] = None

@dataclass
class GenericViewConfigLoader:
    """Loads the view config by using the automatic init of dataclasses"""

    view_config: ViewConfig
