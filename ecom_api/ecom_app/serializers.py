from rest_framework import serializers
from .models import Product, Order, OrderItem, User
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    status_detail = serializers.SerializerMethodField(method_name = "status", read_only = True)
    class Meta:
        model = User
        fields = ("username", "email", "is_authenticated", "status_detail")

    def status(self, obj):
        orders = obj.orders.all()
        for order in orders:
            if order.status == "Confirmed":
                yield {"Confirmed" : order.order_id}
            continue

        #exclude = ("password", "orders")
        #fields = "__all__"

    def status(self, obj):
        orders = obj.orders.filter(status = "Confirmed")
        confirmed_orders = []
        for order in orders:
            confirmed_orders.append(order.order_id)

        return {"Confirmed_orders" : confirmed_orders}



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id","name", "price", "stock")

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    





    
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    items = OrderItemCreateSerializer(many = True, required = False)
    order_id = serializers.UUIDField(read_only = True)

    
    class Meta:
        model = Order
        fields = ("order_id", "user", "status", "items")

        extra_kwargs = {"user":{"read_only": True}}

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        with transaction.atomic():

            order = Order.objects.create(**validated_data)

            for item in items_data:
                OrderItem.objects.create(order=order, **item)
        
        return order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)


        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if items_data:

                instance.items.all().delete()

                for item in items_data:
                    OrderItem.objects.create(order= instance, **item)

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    #product = ProductSerializer()
    product = serializers.ReadOnlyField(source = "product.name")
    #product = serializers.PrimaryKeyRelatedField(queryset= Product.objects.all(), write_only= True)
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")

    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = "user.username")
    items = OrderItemSerializer(many = True)
    order_id = serializers.UUIDField(read_only = True)
    total = serializers.ReadOnlyField()
    
    #order_detail = serializers.SerializerMethodField(method_name = "details")

    # def create(self, validated_data):
    #     items = validated_data.pop("items")
    #     order = Order.objects.create(**validated_data)

    #     for item in items:
    #         OrderItem.objects.create(order=order, product = item["product"], quantity = item["quantity"])

    #     return order


    # def details(self,obj):
    #     items = obj.items.all()
    #     for item in items:
    #         yield {"name":item.product.name,
    #                 "price":item.product.price,
    #                 "quantity":item.quantity} 



    # def get_total(self,obj):
    #     order_items = obj.items.all()
    #     return sum(order_item.sub_total for order_item in order_items)


    class Meta:
        model = Order
        fields = ("order_id", "user", "created_at", "status", "total", "items")

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many= True)
    total = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits = 10, decimal_places = 2)

