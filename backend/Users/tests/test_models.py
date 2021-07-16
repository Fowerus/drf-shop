import jwt

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from Users.models import User



class TestUsersModels(APITestCase):

	def setUp(self):
		self.user = get_user_model()(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com")
		self.user.set_password("john")
		self.user.save()


	def testUser_meta_atributes(self):
		#email
		self.assertEquals(self.user._meta.get_field('email').verbose_name, 'email')
		self.assertTrue(self.user._meta.get_field('email').unique)
		self.assertFalse(self.user._meta.get_field('email').blank)

		#image
		self.assertEquals(self.user._meta.get_field('image').verbose_name, 'image')
		self.assertEquals(self.user._meta.get_field('image').upload_to, './static/Users/images')
		self.assertEquals(self.user._meta.get_field('image').default, '../static/Users/images/default-user-image.jpeg')
		self.assertEquals(self.user._meta.get_field('image').size,[225,225])
		self.assertTrue(self.user._meta.get_field('image').blank)

		#last_name
		self.assertEquals(self.user._meta.get_field('last_name').verbose_name, 'last_name')
		self.assertEquals(self.user._meta.get_field('last_name').max_length, 150)
		
		#first_name
		self.assertEquals(self.user._meta.get_field('first_name').verbose_name, 'first_name')
		self.assertEquals(self.user._meta.get_field('first_name').max_length, 150)

		#date_creating
		self.assertEquals(self.user._meta.get_field('date_creating').verbose_name, 'date_creating')
		self.assertTrue(self.user._meta.get_field('date_creating').auto_now_add)

		#is_staff
		self.assertFalse(self.user._meta.get_field('is_staff').default)

		#is_superself.user
		self.assertFalse(self.user._meta.get_field('is_superuser').default)

		#is_active
		self.assertTrue(self.user._meta.get_field('is_active').default)

		#self.USERNAME_FIELD
		self.assertEquals(self.user.USERNAME_FIELD, 'email')

		#REQUIRED_FIELDS
		self.assertEquals(self.user.REQUIRED_FIELDS, ('last_name','first_name'))


	def testAvailableMethods(self):
		self.user = User.objects.get(id = 1000)
		self.user_fields = {
						'id':self.user.id,
						'last_name':self.user.last_name,
						'first_name':self.user.first_name,
						'image':str(self.user.image),
						'email':self.user.email
					   }
		all_methods = dir(self.user)

		#Checking personal methods
		[self.assertIn(i,all_methods) for i in ['_generate_jwt_token', 'get_short_name', 'get_full_name', 'token']]
		self.assertEquals(type(self.user.token),str)
		self.assertEquals(self.user.token, self.user._generate_jwt_token())
		self.assertEquals(self.user.get_full_name(), self.user.last_name + ' ' + self.user.first_name)
		self.assertEquals(self.user.get_short_name(), self.user.first_name)

		jwt_decode = jwt.decode(self.user._generate_jwt_token(), settings.SECRET_KEY, algorithms=['HS256'])

		#Checking what the token contains
		self.assertEquals(set(jwt_decode.keys()), set(self.user_fields.keys()))
		[self.assertEquals(self.user_fields[i],jwt_decode[i]) for i in jwt_decode.keys()]

		#Meta class attributs cheking
		self.assertEquals(self.user._meta.verbose_name_plural,'Users')
		self.assertEquals(self.user._meta.verbose_name,'User')
		self.assertEquals(self.user._meta.ordering,['-date_creating'])