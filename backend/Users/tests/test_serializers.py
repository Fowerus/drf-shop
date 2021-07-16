from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Users.models import User
from Users.serializers import *



class TestUsersSerializers(APITestCase):

	def setUp(self):
		self.user = get_user_model()(id = 1000, first_name = 'John', last_name = 'Smith', email = 'here_is_johnny@gmail.com')
		self.user.set_password('john')
		self.user.save()


	def testUserRetrieveSerializer(self):
		serializer = UserRetrieveSerializer(self.user)

		#Cheсking the `fields` in serailzier meta-class
		self.assertEquals(serializer.Meta.fields,['id','email','last_name','first_name', 'image', 'date_creating'])

		#Checking the `model` in serializer meta-class
		self.assertEquals(serializer.Meta.model, User)


	def testUserLoginSerializer(self):
		data = {'email':'here_is_johnny@gmail.com', 'password':'john'}
		serializer = UserLoginSerializer(data = data)

		#Checking serializer fields
		self.assertEquals(set(serializer.fields.keys()), {'email','password', 'token'})

		#Checking the attributes of serializer fields
		#email
		self.assertTrue(serializer.fields['email'].write_only)

		#password
		self.assertEquals(serializer.fields['password'].max_length, 128)
		self.assertTrue(serializer.fields['password'].write_only)

		#token
		self.assertEquals(serializer.fields['token'].max_length, 255)
		self.assertTrue(serializer.fields['token'].read_only)

		#Cheking of data validation and the presence of the token in the serializer.data  
		self.assertTrue(serializer.is_valid())
		self.assertTrue('token' in serializer.data)


	def tearDown(self):
		self.user.delete()


	def testUserRegistrationSerializer(self):
		data = {'email':'test_user@gmail.com', 'first_name':'0010001us','last_name':'er','password':'test_user_password'}
		serializer = UserRegistrationSerializer(data = data)

		#Cheсking the `fields` in serailzier meta-class
		self.assertEquals(serializer.Meta.fields, ['email','last_name','first_name','password'])

		#Checking password field in serializer
		self.assertTrue('password' in list(serializer.fields.keys()))

		#Checking the attrubutes of serializer fields
		self.assertEquals(serializer.fields['password'].max_length, 128)
		self.assertEquals(serializer.fields['password'].min_length, 8)
		self.assertTrue(serializer.fields['password'].write_only)

		#Checking of data validation
		self.assertTrue(serializer.is_valid())

		serializer.save()
		user = get_user_model().objects.get(email = 'test_user@gmail.com')

		#Checking a new user
		self.assertTrue(user.check_password('test_user_password'))