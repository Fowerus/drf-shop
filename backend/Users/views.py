import jwt

from django.conf import settings
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import * 
from .models import User



class CheckTokenAPIView(APIView):

	def post(self, request, token):
		try:
			token_decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

			if 'id' in token_decode and 'email' in token_decode:
				return Response(status = status.HTTP_200_OK)

		except:
			return Response(status = status.HTTP_400_BAD_REQUEST)



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

			return Response(serializer.data, status = status.HTTP_200_OK)

		return Response(status = status.HTTP_400_BAD_REQUEST)



class UserRetrieveUpdateAPIView(APIView):
	serializer_class = UserRetrieveSerializer

	def get(self, request, user_id):
		try:
			current_user = User.objects.get(id = user_id)
		except:
			return Response(status = status.HTTP_400_BAD_REQUEST)

		serializer = self.serializer_class(current_user)
		return Response(serializer.data, status = status.HTTP_200_OK)


	def patch(self, request, user_id):
		if 'password' in request.data:

			mes = {
				'error':{},
				'success':{}
			}

			if current_user.check_password(request.data['password']):
				try:
					current_user = User.objects.get(id = user_id)
				except:
					return Response(status = status.HTTP_400_BAD_REQUEST)

				if 'first_name' in request.data or 'last_name' in request.data:
					if 'first_name' in request.data:
						if len(str(request.data['first_name'])) > 1:
							current_user.first_name = request.data['first_name']
							mes['success']['first_name'] = 'First name changed successfully'
						else:
							mes['error']['first_name'] = 'New first name is too short'

					if 'last_name' in request.data:
						if len(str(request.data['last_name'])) > 1:
							current_user.last_name = request.data['last_name']
							mes['success']['last_name'] = 'Second name changed successfully'
						else:
							mes['error']['last_name'] = 'New second name is too short'

				if 'email' in request.data:
					new_user_email = current_user.normalize_email(request.data['email'])
					check_email = User.objects.filter(email = new_user_email)

					if len(check_email) == 0:
						current_user.email = new_user_email
						mes['success']['email'] = 'Email address changed successfully'
					else:
						mes['error']['email'] = 'The selected email address is already in use'

				if 'new_password' in request.data:
					if len(str(request.data['password'])) >= 8:
						current_user.make_password(str(request.data['new_password']))
					else:
						mes['error']['new_password'] = 'New password is too short'

				if len(mes['success']) != 0:
					current_user.save()
					
				return Response(mes, status = status.HTTP_200_OK)

			else:
				return Response({'error':{'password':'The password you entered is incorrect'}}, status = status.HTTP_400_BAD_REQUEST)