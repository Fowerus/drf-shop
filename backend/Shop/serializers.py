import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .models import *
from Users.serializers import UserViewSerializer



class AdditionalSerializer(serializers.ModelSerializer):

	class CurrencySerializer(serializers.ModelSerializer):
		class Meta:
			model = Currency
			fields = ['id', 'name', 'system_id']

	class CategorySerializer(serializers.ModelSerializer):
		class Meta:
			model = Category
			fields = ['id', 'name']



class ProductSerializer(serializers.ModelSerializer):
	category = AdditionalSerializer.CategorySerializer()
	currency = AdditionalSerializer.CurrencySerializer()

	def create(self, validated_data):
		product = Product.objects.create(**validated_data)
		return product

	class Meta:
		model = Product
		fields = ['id', 'name', 'category', 'description','currency', 'cost', 'image']



class CurrentProductSerializer(serializers.ModelSerializer):
	category = AdditionalSerializer.CategorySerializer()
	currency = AdditionalSerializer.CurrencySerializer()
	
	class Meta:
		model = Product
		fields = ['id', 'name', 'category', 'description','currency', 'cost', 'image']



class TestimonialSerializer(serializers.ModelSerializer):

	class ListSerializer(serializers.ModelSerializer):
		product = CurrentProductSerializer()
		user = UserViewSerializer()

		class Meta:
			model = Testimonial
			fields = ['id', 'product', 'stars_count', 'description', 'user', 'date_creating']


	class CreateSerializer(serializers.ModelSerializer):

		def create(self, validated_data):
			return Testimonial.objects.create(**validated_data)

		def get_current_testimonial(self, id):
			return Testimonial.objects.get(id = id)
			
		class Meta:
			model = Testimonial
			fields = ['id', 'product', 'stars_count', 'description', 'user', 'date_creating']


	class Meta:
		model = Testimonial
		fields = ['id', 'product', 'stars_count', 'description', 'user', 'date_creating']



class CartSerializer(serializers.ModelSerializer):

	class ListSerializer(serializers.ModelSerializer):
		product = CurrentProductSerializer()
		user = UserViewSerializer()

		class Meta:
			model = Cart
			fields = ['id', 'product', 'user', 'date_creating']


	class CreateSerializer(serializers.ModelSerializer):

		def create(self, validated_data):
			return Cart.objects.create(**validated_data)

		def get_current_product(self, id):
			return Cart.objects.get(id = id)

		class Meta:
			model = Cart
			fields = ['id', 'product', 'user', 'date_creating']

	class Meta:
		model = Cart
		fields = ['id', 'product', 'user', 'date_creating']



class OrderSerializer(serializers.ModelSerializer):

	class ListSerializer(serializers.ModelSerializer):
		user = UserViewSerializer()

		class Meta:
			model = Order
			fields = ['id', 'user', 'hash_code', 'url', 'order_code', 'order_cost', 'paid', 'date_creating']


	class Create(serializers.ModelSerializer):

		def create(self, validated_date):
			return Order.objects.create(**validated_date)

		class Meta:
			model = Order
			fields = ['id', 'user', 'hash_code', 'url', 'order_code', 'order_cost', 'paid', 'date_creating']



class GroupSerializer(serializers.ModelSerializer):

	class ListSerializer(serializers.ModelSerializer):
		user = UserViewSerializer()
		product = CurrentProductSerializer()

		class Meta:
			model = Group
			fields = ['id', 'user', 'product', 'date_creating']


	class CreateSerializer(serializers.ModelSerializer):

		def create(self, validated_date):
			return Group.objects.create(**validated_date)

		class Meta:
			model = Group
			fields = ['id', 'user', 'product', 'order', 'date_creating']