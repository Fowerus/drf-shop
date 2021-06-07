from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import * 
from .models import User





class UserRegistrationAPIView(APIView):
	serializer_class = UserRegistrationSerializer

	def post(self, request):
		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		return Response(status = status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, request):
		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			serializer = serializer.data

			serializer_user = UserViewSerializer(User.objects.get(email = request.data['email'])).data

			serializer.update(serializer_user)

			return Response(serializer, status = status.HTTP_200_OK)

		return Response(status = status.HTTP_400_BAD_REQUEST)



class UserRetrieveDestroyAPIView(APIView):
	serializer_class = UserRetrieveDestroySerializer

	