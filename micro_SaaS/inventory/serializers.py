from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Business, Product, StockTransaction


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


class BusinessSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Business
        fields = ['id', 'name', 'address', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


class ProductSerializer(serializers.ModelSerializer):
    business = serializers.ReadOnlyField(source='business.id')

    class Meta:
        model = Product
        fields = [
            'id', 'business', 'name', 'sku', 'category',
            'current_quantity', 'reorder_level', 'unit', 'supplier_name'
        ]
        read_only_fields = ['id', 'business', 'current_quantity']


class StockTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    business = serializers.ReadOnlyField(source='business.id')

    class Meta:
        model = StockTransaction
        fields = ['id', 'product', 'product_name', 'business', 'type', 'quantity', 'created_at']
        read_only_fields = ['id', 'business', 'created_at']

    def validate(self, data):
        product = data.get('product')
        transaction_type = data.get('type')
        quantity = data.get('quantity')

        if transaction_type == 'Out' and product.current_quantity < quantity:
            raise serializers.ValidationError({
                'quantity': f'Insufficient stock. Current quantity is {product.current_quantity}.'
            })
        return data
