"""This file is responsible for handling the factories for the generic views"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from rest_framework.views import APIView

from .generic_views import UpdateView, CreateView, ListView, DetailView, DeleteAllView
from shared.configs.view_config import GenericViewConfigLoader, ViewConfig


class ViewFactory(ABC):
    """Abstract factory that represents generic views.

    This class defines a common interface for creating instances of different views.
    Subclasses of this class must implement the `get_view` method to create and return
    instances of specific views.
    """

    @abstractmethod
    def get_view(self, view_name: str):
        """Returns a new view instance"""


class BaseView(GenericViewConfigLoader, ViewFactory):
    """Concrete factory for creating instances of the generic views"""

    views = {
        'update_view': UpdateView,
        'create_view': CreateView,
        'list_view': ListView,
        'detail_view': DetailView,
        'delete_all_view': DeleteAllView,
    }

    def get_view(self, view_name: str):
        view_class = self.views[view_name]
 
        return view_class(self.view_config)


@dataclass
class GenericViewFactory(APIView):
    """Concrete factory for returning the generic view instances form the
        BaseView factory.
        
        This class takes in a ViewConfig then initializes the BaseView.
        The initialized views can be access through the use of properties
        which return their responding view types.
        """

    view_config: ViewConfig

    def __post_init__(self) -> None:
        self.__base_view = BaseView(view_config=self.view_config)

    @property
    def update_view(self) -> Type[UpdateView]:
        return self.__base_view.get_view('update_view')

    @property
    def create_view(self) -> Type[CreateView]:
        return self.__base_view.get_view('create_view')

    @property
    def list_view(self) -> Type[ListView]:
        return self.__base_view.get_view('list_view')

    @property
    def detail_view(self) -> Type[DetailView]:
        return self.__base_view.get_view('detail_view')

    @property
    def delete_all_view(self) -> Type[DeleteAllView]:
        return self.__base_view.get_view('delete_all_view')
