from rest_framework.response import Response
from rest_framework.request import Request
from abc import ABC, abstractmethod


class UpdateViewInterface(ABC):
    """Absract interface that defines the methods of an UpdateVIew"""

    @abstractmethod
    def put(self, request: Request, pk=None, lookup_query=None) -> Response:
        """Updates the object fully"""

    @abstractmethod
    def patch(self, request: Request, pk=None, look_query=None) -> Response:
        """Updates an object partially"""


class CreateViewInterface(ABC):
    """Abstract interface that defines the methods of a CreateView"""

    @abstractmethod
    def post(self, request: Request) -> Response:
        """Creates an object"""


class ListViewInterface(ABC):
    """Abstract interface that defines the methods of a ListView"""

    @abstractmethod
    def get(self, request: Request) -> Response:
        """Lists all the objects"""


class DetailViewInterface(ABC):
    """Abstract interface that defines the methods of a DetailView"""

    @abstractmethod
    def get(self, request: Request, query: dict) -> Response:
        """Gets a single object"""


class DeleteViewInterface(ABC):
    """Abstract interface that defines the methods of a DeleteView"""

    @abstractmethod
    def delete(self, request: Request) -> Response:
        """Either deletes a single object or all objects"""
