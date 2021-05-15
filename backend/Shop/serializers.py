import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .models import *
from Users.serializers import UserViewSerializer



class AdditionalProductSerializer(serializers.ModelSerializer):

	class CurrencySerializer(serializers.ModelSerializer):
		class Meta:
			model = Currency
			fields = ['id', 'name', 'system_id']

	class CategorySerializer(serializers.ModelSerializer):
		class Meta:
			model = Category
			fields = ['id', 'name']

	# class ImageSerializer(serializers.Serializer):
	# 	image = serializers.ImageField()

	# 	def update(self, validated_data):

	# 		image = validated_data.get('image', None)

	# 		if image is not None:
	# 			image = open(image, "rb")
	# 			return str(image)




class AllProductsSerializer(serializers.ModelSerializer):
	category = AdditionalProductSerializer.CategorySerializer()
	currency = AdditionalProductSerializer.CurrencySerializer()

	# image = AdditionalProductSerializer.ImageSerializer()

	def create(self, validated_data):
		product = Product.objects.create(**validated_data)
		return product

	class Meta:
		model = Product
		fields = ['id', 'name', 'category', 'description','currency', 'cost', 'image']



class CurrentProductSerializer(serializers.ModelSerializer):
	category = AdditionalProductSerializer.CategorySerializer()
	currency = AdditionalProductSerializer.CurrencySerializer()
	
	class Meta:
		model = Product
		fields = ['id', 'name', 'category', 'description','currency', 'cost', 'image']



class TestimonialSerializer(serializers.ModelSerializer):
	product = CurrentProductSerializer()
	user = UserViewSerializer()

	class Meta:
		model = Testimonial
		fields = ['id', 'product', 'stars_count', 'description', 'user', 'date_creating']