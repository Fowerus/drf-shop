from django.test import TestCase
from Users.models import User
from Users.serializers import *



class TestSerializers(TestCase):

	def setUp(self):
		self.user = User(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com")
		self.user.set_password("john")
		self.user.save()


	def testUserRetrieveSerializer(self):
		self.user = User.objects.get(id = 1000)
		serializer_data = UserRetrieveSerializer(self.user).data
		keys = [i for i in serializer_data.keys()]

		#Cheking all keys in serializer.data
		self.assertEquals(set(keys),{"id","email","last_name","first_name", "image", "date_creating"})


	def testUserLoginSerializer(self):
		data = {"email":"here_is_johnny@gmail.com", "password":"john"}
		serializer = UserLoginSerializer(data = data)

		#Cheking of data validation and the presence of the token in the serializer.data  
		self.assertTrue(serializer.is_valid())
		self.assertTrue("token" in serializer.data)


	def tearDown(self):
		self.user.delete()


	def testUserRegistrationSerializer(self):
		data = {"email":"test_user@gmail.com", "first_name":"0010001us","last_name":"er","password":"test_user_password"}
		serializer = UserRegistrationSerializer(data = data)

		#Checking of data validation
		self.assertTrue(serializer.is_valid())

		serializer.save()
		user = User.objects.get(email = "test_user@gmail.com")

		#Checking a new user
		self.assertTrue(user.check_password('test_user_password'))