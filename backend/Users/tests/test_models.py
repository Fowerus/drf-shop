import jwt

from django.test import TestCase
from django.conf import settings

from Users.models import User
from Users.serializers import *



class TestModels(TestCase):

	@classmethod
	def setUpTestData(cls):
		user = User(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com")
		user.set_password("john")
		user.save()


	def testUser_meta_atributes(self):
		user = User.objects.get(id = 1000)

		#email
		self.assertEquals(user._meta.get_field('email').verbose_name, 'email')
		self.assertTrue(user._meta.get_field('email').unique)
		self.assertFalse(user._meta.get_field('email').blank)

		#image
		self.assertEquals(user._meta.get_field('image').verbose_name, 'image')
		self.assertEquals(user._meta.get_field('image').upload_to, './static/Users/images')
		self.assertEquals(user._meta.get_field('image').default, '../static/Users/images/default-user-image.jpeg')
		self.assertEquals(user._meta.get_field('image').size,[225,225])
		self.assertTrue(user._meta.get_field('image').blank)

		#last_name
		self.assertEquals(user._meta.get_field('last_name').verbose_name, 'last_name')
		self.assertEquals(user._meta.get_field('last_name').max_length, 150)
		
		#first_name
		self.assertEquals(user._meta.get_field('first_name').verbose_name, 'first_name')
		self.assertEquals(user._meta.get_field('first_name').max_length, 150)

		#date_creating
		self.assertEquals(user._meta.get_field('date_creating').verbose_name, 'date_creating')
		self.assertTrue(user._meta.get_field('date_creating').auto_now_add)

		#is_staff
		self.assertFalse(user._meta.get_field('is_staff').default)

		#is_superuser
		self.assertFalse(user._meta.get_field('is_superuser').default)

		#is_active
		self.assertTrue(user._meta.get_field('is_active').default)

		#USERNAME_FIELD
		self.assertEquals(user.USERNAME_FIELD, 'email')

		#REQUIRED_FIELDS
		self.assertEquals(user.REQUIRED_FIELDS, ('last_name','first_name'))


	def testAvailableMethods(self):
		user = User.objects.get(id = 1000)
		user_fields = {'id':user.id,
					   'last_name':user.last_name,
					   'first_name':user.first_name,
					   'image':str(user.image),
					   'email':user.email
					   }
		all_methods = dir(user)

		#Checking personal methods
		[self.assertIn(i,all_methods) for i in ['_generate_jwt_token', 'get_short_name', 'get_full_name', 'token']]
		self.assertEquals(type(user.token),str)
		self.assertEquals(user.token, user._generate_jwt_token())
		self.assertEquals(user.get_full_name(), user.last_name + ' ' + user.first_name)
		self.assertEquals(user.get_short_name(), user.first_name)

		jwt_decode = jwt.decode(user._generate_jwt_token(), settings.SECRET_KEY, algorithms=['HS256'])

		#Checking what the token contains
		self.assertEquals(set(jwt_decode.keys()), set(user_fields.keys()))
		[self.assertEquals(user_fields[i],jwt_decode[i]) for i in jwt_decode.keys()]

		#Meta class attributs cheking
		self.assertEquals(user._meta.verbose_name_plural,'Users')
		self.assertEquals(user._meta.verbose_name,'User')
		self.assertEquals(user._meta.ordering,['-date_creating'])