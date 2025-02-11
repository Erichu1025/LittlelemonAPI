from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth import get_user_model

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    ) 
    class Meta:
        model=MenuItem
        fields=['id','title','price','category','featured','category_id']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, label="User"
    )
    menuitem=serializers.StringRelatedField()
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menuitem', write_only=True, label="Menu item"
    ) 
    class Meta:
        model=Cart
        fields=['id','user','user_id','menuitem','menuitem_id','quantity','unit_price']
        read_only_fields = ['unit_price']  # Make unit_price read-only

    def create(self, validated_data):
        """
        Override the create method to set unit_price automatically
        based on the selected menuitem.
        """
        menuitem = validated_data['menuitem']
        validated_data['unit_price'] = menuitem.price  # Set the price from the MenuItem model
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, label="User"
    )    
    delivery_crew = serializers.StringRelatedField()  
    delivery_crew_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='delivery_crew', write_only=True, label="Delivery crew"
    )    
    class Meta:
        model=Order
        fields=['id','user','user_id','delivery_crew','delivery_crew_id','status','total','date']
        read_only_fields = ['user', 'total']

    def create(self, validated_data):
        """
        Override the create method to calculate the total
        and automatically assign the user if not provided.
        """
        total = 0
        order = Order.objects.create(**validated_data)
        
        # Logic to calculate the total (e.g., summing order items)
        for item in order.orderitem_set.all():  # Assuming a reverse relation to OrderItem
            total += item.price
        
        order.total = total
        order.save()
        return order
    


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField()  
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='order', write_only=True, label="Order"
    )        
    menuitem = serializers.StringRelatedField()
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menuitem', write_only=True, label="Menu item"
    ) 

    total_price = serializers.SerializerMethodField()

    class Meta:
        model=OrderItem
        fields=['id','order','order_id','menuitem','menuitem_id','quantity','unit_price','price','total_price']

    def get_total_price(self, obj):
        """Calculate total price for the cart item."""
        return obj.quantity * obj.unit_price