"""This file is responsible for making store view factories"""

from rest_framework.views import APIView

from shared.factories.view_factory import GenericViewFactory, ViewConfig
from store_app.models import Order, Billing
from store_app.serializers import BillingSerializer, OrderSerializer


class StoreViewFactory(APIView):
    """Concrete store view factory that initializes views with the use of the
        GenericViewFactory that takes in a view config"""

    _order_view_config = ViewConfig(
        serializer_class=OrderSerializer, model=Order, response_name="orders",
        delete_message="Orders removed"
    )

    billing_view_config = ViewConfig(
        serializer_class=BillingSerializer, model=Billing, response_name="billings",
        delete_message="Billings removed"
    )

    order_view = GenericViewFactory(view_config=_order_view_config)
    billing_view = GenericViewFactory(view_config=billing_view_config)
