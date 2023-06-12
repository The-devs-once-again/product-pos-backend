from django.http import JsonResponse
from rest_framework.request import Request
from abc import ABC, abstractmethod


class UpdateViewInterface(ABC):
    """Absract interface that defines the methods of an UpdateVIew"""

    def update(self, request: Request, pk=None, look_query=None, partial=False) -> JsonResponse:  # noqa: E501
        """Gets the object to be updated"""

    @abstractmethod
    def put(self, request: Request, pk=None, look_query=None) -> JsonResponse:
        """Updates the object fully"""

    @abstractmethod
    def patch(self, request: Request, pk=None, look_query=None) -> JsonResponse:
        """Updates an object partially"""

    @abstractmethod
    def delete(self, request: Request, pk=None, look_query=None) -> JsonResponse:
        """Deletes a single object"""


class CreateViewInterface(ABC):
    """Abstract interface that defines the methods of a CreateView"""

    @abstractmethod
    def post(self, request: Request) -> JsonResponse:
        """Creates an object"""


class ListViewInterface(ABC):
    """Abstract interface that defines the methods of a ListView"""

    @abstractmethod
    def get(self, request: Request) -> JsonResponse:
        """Lists all the objects"""


class DetailViewInterface(ABC):
    """Abstract interface that defines the methods of a DetailView"""

    @abstractmethod
    def get(self, request: Request, query: dict) -> JsonResponse:
        """Gets a single object"""


class DeleteAllViewInterface(ABC):
    """Abstract interface that defines the methods of a DeleteAllView"""

    @abstractmethod
    def delete(self, request: Request) -> JsonResponse:
        """Deletes all objects"""
