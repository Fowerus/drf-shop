from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from Shop.models import *




class UserRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','email','last_name','first_name', 'image', 'date_creating']



class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=128, min_length=8, write_only=True)

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)


	class Meta:
		model = User
		fields = ['email','last_name','first_name','password']



class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField(write_only=True)
	password = serializers.CharField(max_length=128, write_only=True)

	token = serializers.CharField(max_length=255, read_only=True)


	def validate(self, data):
		email = data.get('email',None)
		password = data.get('password',None)

		if email is None:
			return Response(status = status.HTTP_404_NOT_FOUND)

		if password is None:
			return Response(status = status.HTTP_404_NOT_FOUND)

		user = authenticate(email = email, password = password)

		if user is None:
			return Response(status = status.HTTP_404_NOT_FOUND)

		if not user.is_active:
			return Response(status = status.HTTP_404_NOT_FOUND)

		validated_data = {'token':user.token}

		return validated_data