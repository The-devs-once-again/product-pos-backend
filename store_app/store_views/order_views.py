from django.http import JsonResponse
from rest_framework.request import Request

from shared.utils.api_utils import RequestsUtils
from store_app.store_factories.store_view_factory import StoreViewFactory


def get_order_id(lookup_value: str) -> dict:
    return RequestsUtils.get_query_params(lookup_key="order_id", lookup_value=lookup_value)


class OrderUpdateView(StoreViewFactory):
    def put(self, request: Request, order_id: str) -> JsonResponse:
        return self.order_view.update_view.update(request, lookup_query=get_order_id(order_id))

    def patch(self, request: Request, order_id: str) -> JsonResponse:
        return self.order_view.update_view.patch(request, lookup_query=get_order_id(order_id))

    def delete(self, request: Request, order_id: str) -> JsonResponse:
        return self.order_view.update_view.delete(request, lookup_query=get_order_id(order_id))


class OrderCreateView(StoreViewFactory):
    def post(self, request: Request) -> JsonResponse:
        return self.order_view.create_view.post(request)


class OrderListView(StoreViewFactory):
    def get(self, request: Request) -> JsonResponse:
        return self.order_view.list_view.get(request)


class OrderDetailView(StoreViewFactory):
    def get(self, request: Request, order_id: str) -> JsonResponse:
        return self.order_view.detail_view.get(request, get_order_id(order_id))


class OrderDeleteAllView(StoreViewFactory):
    def delete(self, request: Request) -> JsonResponse:
        return self.order_view.delete_all_view.delete(request)
