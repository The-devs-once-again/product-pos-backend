"""This file is responsible for handling the object factories"""

from abc import abstractmethod, ABC
from typing import Any

from django.db import models


class ObjectFactory(ABC):
    """Abstract factory that represents creation and updating of an object"""

    @abstractmethod
    def create_object(self, validated_data) -> models.Model:
        """Returns a model"""

    @abstractmethod
    def update_object(self, instance, validated_data) -> Any:
        """Updates the object"""
