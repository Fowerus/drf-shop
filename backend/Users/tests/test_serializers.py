import jwt
from django.test import TestCase
from Users.models import User
from Users.serializers import *



class TestSerializers(TestCase):

	@classmethod
	def setUpTestData(cls):
		User.objects.create(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com", password = "john")


	def testUserViewSerializer(self):
		user = User.objects.get(id = 1000)
		serializer_data = UserViewSerializer(user).data
		keys = [i for i in serializer_data.keys()]
		self.assertEquals(set(keys),{"id","email","last_name","first_name", "image", "date_creating"})


	def testUserRegistrationSerializer(self):
		data = {"email":"test_user@gmail.com", "first_name":"0010001us","last_name":"er","password":"test_user_password"}
		serializer = UserRegistrationSerializer(data = data)
		self.assertTrue(serializer.is_valid())

		serializer.save()
		user = User.objects.filter(email = "test_user@gmail.com").filter(first_name = "0010001us").filter(last_name = "er").first()
		self.assertTrue(user.check_password('test_user_password'))


	def testUserLoginSerializer(self):
		data = {"email":"here_is_johnny@gmail.com", "password":"john"}
		serializer = UserLoginSerializer(data = data)
		self.assertTrue(serializer.is_valid())
		self.assertTrue("token" in serializer.data)