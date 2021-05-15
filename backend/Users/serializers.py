import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from Shop.models import *



class UserViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'last_name', 'first_name', 'image']



class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=128, min_length=8, write_only=True)

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

	class Meta:
		model = User
		fields = ['username','email','last_name','first_name','password']



class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField(write_only=True)
	password = serializers.CharField(max_length=128, write_only=True)

	username = serializers.CharField(max_length=255, read_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		email = data.get('email',None)
		password = data.get('password',None)


		if email is None:
			return Response(status = status.HTTP_404_NOT_FOUND)

		if password is None:
			return Response(status = status.HTTP_404_NOT_FOUND)


		try:
			current_user = User.objects.get(email = email)

			user = authenticate(username = current_user.username, email = email, password = password)


			if user is None:
				return Response(status = status.HTTP_404_NOT_FOUND)

			elif not user.is_active:
				return Response(status = status.HTTP_404_NOT_FOUND)


			validated_data = user.token
			validated_data.setdefault('token', jwt.encode(user.token,settings.SECRET_KEY, algorithm = 'HS256'))

			return validated_data


		except:
			return {'error': 'This user did not exist'}