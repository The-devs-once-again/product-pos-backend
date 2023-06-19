"""This file is responsible for making product factories"""

from ..models import Size, AddOn, Variation, Product
from shared.factories.object_factory import ObjectFactory


class ProductFactory(ObjectFactory[Product]):
    """
    
    Concrete product object factory creates an item object. This factory implements the
    abstract ObjectFactory.
    
    """

    def create_object(self, validated_data) -> Product:
        """
        
        Creates product object then returns a product instance.

        """

        variation_data = validated_data.pop('variation', None)

        if variation_data:
            size_data_list = variation_data.pop('size', [])
            add_on_data_list = variation_data.pop('add_on', [])

            size_list = []
            for size_data in size_data_list:
                size_price = size_data.pop('size_price')
                size_list.append(Size.objects.create(size_price=size_price, **size_data))

            add_on_list = []
            for add_on_data in add_on_data_list:
                add_on_price = add_on_data.pop('add_on_price')
                add_on_list.append(AddOn.objects.create(add_on_price=add_on_price, **add_on_data))

            variation = Variation.objects.create()

            if size_list:
                variation.size.set(size_list)
            if add_on_list:
                variation.add_on.set(add_on_list)
        else:
            variation = None

        return Product.objects.create(variation=variation, **validated_data)

    @staticmethod
    def _update_variation(instance, variation_data):
        """
        
        A static method that updates the variation object which contains the
        size and add_on lists

        """

        size_data_list = variation_data.get('size', [])
        add_on_data_list = variation_data.get('add_on', [])

        size_list = []
        for size_data in size_data_list:
            size_price = size_data.pop('size_price', None)
            
            if size_price is not None:
                size_list.append(Size.objects.create(size_price=size_price, **size_data))

        add_on_list = []
        for add_on_data in add_on_data_list:
            add_on_price = add_on_data.pop('add_on_price', None)
            add_on_list.append(AddOn.objects.create(add_on_price=add_on_price, **add_on_data))

        if instance.variation is None:
            instance.variation = Variation.objects.create()

        instance.variation.size.set(size_list)
        instance.variation.add_on.set(add_on_list)

    def update_object(self, instance, validated_data) -> Product:
        """
        
        Updates the existing product instance then returns a updated
        product instance.

        """

        instance.product_name = validated_data['product_name']
        instance.product_price = validated_data['product_price']
        instance.product_type = validated_data['product_type']
        instance.category = validated_data['category']

        variation_data = validated_data.get('variation')

        if variation_data is not None:
            self._update_variation(instance, variation_data)

        instance.save()

        return instance
