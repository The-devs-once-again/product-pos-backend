"""This file is responsible for handling the factories for the generic views"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rest_framework.views import APIView

from .generic_views import UpdateView, CreateView, ListView, DetailView, DeleteAllView
from shared.configs.view_config import GenericViewConfigLoader, ViewConfig


@dataclass
class ViewFactory(ABC):
    """Abstract factory that represents generic views"""

    @abstractmethod
    def get_update_view(self) -> UpdateView:
        """Returns an UpdateView"""

    @abstractmethod
    def get_create_view(self) -> CreateView:
        """Returns a CreateView"""

    @abstractmethod
    def get_list_view(self) -> ListView:
        """Returns a ListView"""

    @abstractmethod
    def get_detail_view(self) -> DetailView:
        """Returns a DetailView"""

    @abstractmethod
    def get_delete_all_view(self) -> DeleteAllView:
        """Returns a new delete all objects view"""


class BaseView(GenericViewConfigLoader, ViewFactory):
    """Concrete factory for creating instances of the generic views"""

    def get_update_view(self) -> UpdateView:
        return UpdateView(self.view_config)

    def get_create_view(self) -> CreateView:
        return CreateView(self.view_config)

    def get_list_view(self) -> ListView:
        return ListView(self.view_config)

    def get_detail_view(self) -> DetailView:
        return DetailView(self.view_config)

    def get_delete_all_view(self) -> DeleteAllView:
        return DeleteAllView(self.view_config)


@dataclass
class GenericViewFactory(APIView):
    """Concrete factory for returning the generic view instances form the BaseView factory. It also
        takes in a view_config which then shares across all generic views"""

    view_config: ViewConfig

    def __post_init__(self):
        self.base_view = BaseView(view_config=self.view_config)

    @property
    def update_view(self):
        return self.base_view.get_update_view()

    @property
    def create_view(self):
        return self.base_view.get_create_view()

    @property
    def list_view(self):
        return self.base_view.get_list_view()

    @property
    def detail_view(self):
        return self.base_view.get_detail_view()

    @property
    def delete_all_view(self):
        return self.base_view.get_delete_all_view()
