"""This file is responsible for handling the object factories"""

from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from django.db import models

ModelType = TypeVar('ModelType', bound=models.Model)

class ObjectFactory(ABC, Generic[ModelType]):
    """Abstract factory that represents creation and updating of an object"""

    @abstractmethod
    def create_object(self, validated_data) -> ModelType:
        """Returns a type of a model"""

    @abstractmethod
    def update_object(self, instance, validated_data) -> ModelType:
        """Updates the object"""
