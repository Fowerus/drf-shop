import jwt

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.base_user import BaseUserManager

from .serializers import * 
from .models import User



class CheckTokenAPIView(APIView):

	def post(self, requests, token):
		try:
			token_decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

			if 'id' in token_decode and 'email' in token_decode:
				return Response(status = status.HTTP_200_OK)

		except:
			return Response(status = status.HTTP_400_BAD_REQUESTs)



class UserRegistrationAPIView(APIView):
	serializer_class = UserRegistrationSerializer

	def post(self, requests):
		serializer = self.serializer_class(data = requests.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		return Response(status = status.HTTP_400_BAD_REQUESTs)



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer

	def post(self, requests):
		serializer = self.serializer_class(data = requests.data)
		if serializer.is_valid():

			return Response(serializer.data, status = status.HTTP_200_OK)

		return Response(status = status.HTTP_400_BAD_REQUESTs)



class UserRetrieveUpdateAPIView(APIView):
	serializer_class = UserRetrieveSerializer

	def get(self, requests, user_id):
		try:
			current_user = get_user_model().objects.get(id = user_id)
		except:
			return Response(status = status.HTTP_400_BAD_REQUESTs)

		serializer = self.serializer_class(current_user)
		return Response(serializer.data, status = status.HTTP_200_OK)


	def patch(self, requests, user_id):
		if 'password' in requests.data:

			mes = {
				'error':{},
				'success':{}
			}

			try:
				current_user = get_user_model().objects.get(id = user_id)
			except:
				return Response(status = status.HTTP_400_BAD_REQUESTs)

			if current_user.check_password(requests.data['password']):

				if 'first_name' in requests.data or 'last_name' in requests.data:
					if 'first_name' in requests.data:
						if len(str(requests.data['first_name'])) > 1:
							current_user.first_name = requests.data['first_name']
							mes['success']['first_name'] = 'First name changed successfully'
						else:
							mes['error']['first_name'] = 'New first name is too short'

					if 'last_name' in requests.data:
						if len(str(requests.data['last_name'])) > 1:
							current_user.last_name = requests.data['last_name']
							mes['success']['last_name'] = 'Second name changed successfully'
						else:
							mes['error']['last_name'] = 'New second name is too short'

				if 'email' in requests.data:
					if len(requests.data['email']) >= 12:
						new_user_email = BaseUserManager.normalize_email(requests.data['email'])
						check_email = get_user_model().objects.filter(email = new_user_email)

						if len(check_email) == 0:
							current_user.email = new_user_email
							mes['success']['email'] = 'Email address changed successfully'
						else:
							mes['error']['email'] = 'The selected email address is already in use'
					else:
						mes['error']['email'] = 'New email address is too short'

				if 'new_password' in requests.data:
					if len(str(requests.data['new_password'])) >= 8:
						current_user.set_password(str(requests.data['new_password']))
						mes['success']['new_password'] = 'Password changed successfully'
					else:
						mes['error']['new_password'] = 'New password is too short'

				if len(mes['success']) != 0:
					current_user.save()
					
				return Response(mes, status = status.HTTP_200_OK)

			else:
				return Response({'error':{'password':'The password you entered is incorrect'}}, status = status.HTTP_400_BAD_REQUESTs)