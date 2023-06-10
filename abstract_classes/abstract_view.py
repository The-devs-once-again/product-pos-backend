from abc import abstractmethod, ABC
from django.db import models


class UpdateViewABC(ABC):
    def get_model_class(self, pk=None, look_query=None) -> models.Model:
        pass

    def update(self, request, pk=None, look_query=None, partial=False):
        pass

    @abstractmethod
    def put(self, request, pk=None, look_query=None):
        pass

    @abstractmethod
    def patch(self, request, pk=None, look_query=None):
        pass

    @abstractmethod
    def delete(self, request, pk=None, look_query=None):
        pass


class CreateViewABC(ABC):
    @abstractmethod
    def post(self, request):
        pass


class ListViewABC(ABC):
    @abstractmethod
    def get(self, request):
        pass


class DetailViewABC(ABC):
    @abstractmethod
    def get(self, request, query):
        pass
