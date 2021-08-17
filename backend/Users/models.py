import jwt
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django_resized import ResizedImageField


#User's auth
class UserManager(BaseUserManager):
	def _create_user(self, email, last_name, first_name, password = None, **extra_fields):
		email = self.normalize_email(email)
		user = self.model(email = email, last_name = last_name, first_name = first_name, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)

		return user


	def create_user(self, email, last_name, first_name, password = None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)

		return self._create_user(email = email, last_name = last_name, first_name = first_name, password = password, **extra_fields)


	def create_superuser(self, email, last_name, first_name, password = None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		return self._create_user(email = email, last_name = last_name, first_name = first_name, password = password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(validators = [validators.EmailValidator], unique = True, blank = False, verbose_name = 'email')
	image = ResizedImageField(size = [225,225], upload_to = '../static/Users/images', blank = True, default = '../static/Users/images/default-user-image.jpeg', verbose_name = 'image')
	last_name = models.CharField(max_length = 150, verbose_name = 'last_name')
	first_name = models.CharField(max_length = 150, verbose_name = 'first_name')
	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'date_creating')

	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('last_name','first_name')

	objects = UserManager()


	@property
	def token(self):
		return self._generate_jwt_token()


	def get_full_name(self):
		return self.last_name + ' ' + self.first_name


	def get_short_name(self):
		return self.first_name


	def _generate_jwt_token(self):
		token_encode = jwt.encode({
			'id': self.pk,
			'last_name':self.last_name,
			'first_name':self.first_name,
			'image':str(self.image),
			'email':self.email,
		}, settings.SECRET_KEY, algorithm='HS256')

		return token_encode


	def __str__(self):
		return f'id:{self.id} | first_name:{self.first_name} | email:{self.email}'


	class Meta:
		verbose_name_plural 	= 'Users'
		verbose_name 			= 'User'
		ordering 				= ['-date_creating']
