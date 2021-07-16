from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from ..models import *



class TestShopAPI(APITestCase):

	def setUp(self):
		self.user = get_user_model()(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com")
		self.user.set_password("john")
		self.user.save()


	def testUserLogin(self):
		url = reverse('user-login')
		data = {'email':self.user.email, 'password':self.user.password}
		res = self.client.post(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	def testUserRetrieve(self):
		url = reverse('user-retrieve', args = [self.user.id])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	def testUserUpdate(self):
		url = reverse('user-update', args = [self.user.id])
		data = {'password':'john', 'email':'here_is_bob@gmail.com', 'new_password':'bobbobbo', 'first_name':'bob', 'last_name':'bobber'}
		res = self.client.patch(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		self.assertEquals(len(res.data['success']), len(data)-1)

		#Checking changed data
		self.user = get_user_model().objects.get(id = self.user.id)

		self.assertEquals(self.user.email, data['email'])
		self.assertTrue(self.user.check_password(data['new_password']))
		self.assertEquals(self.user.first_name, data['first_name'])
		self.assertEquals(self.user.last_name, data['last_name'])

		data = {'password':'bobbobbo', 'email':'l.com', 'new_password':'b', 'first_name':'b', 'last_name':'b'}
		res = self.client.patch(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		self.assertEquals(len(res.data['error']), len(data)-1)

		#Checking unchanged data
		self.assertIsNot(self.user.email, data['email'])
		self.assertFalse(self.user.check_password(data['new_password']))
		self.assertIsNot(self.user.first_name, data['first_name'])
		self.assertIsNot(self.user.last_name, data['last_name'])


	def tearDown(self):
		self.user.delete()


	def testUserRegistration(self):
		url = reverse('user-registration')
		data = {'email':'test_user@gmail.com', 'first_name':'0010001us','last_name':'er','password':'test_user_password'}
		res = self.client.post(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)