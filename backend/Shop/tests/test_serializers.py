from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Shop.models import *
from Shop.serializers import *



class TestShopSerializers(APITestCase):

	def setUp(self):
		self.user = get_user_model()(id = 1000, first_name = 'John', last_name = 'Smith', email = 'here_is_johnny@gmail.com')
		self.user.set_password('john')
		self.user.save()


	def testAdditionalSerializer(self):
		currencySerializer = AdditionalSerializer.CurrencySerializer(self.user)
		categorySerializer = AdditionalSerializer.CategorySerializer(self.user)

		#Cheсking the `fields` and `model` in currencySerializer
		self.assertEquals(currencySerializer.Meta.fields,['id', 'name', 'system_id'])
		self.assertEquals(currencySerializer.Meta.model, Currency)

		#Cheсking the `fields` and `model` in categorySerializer meta-class
		self.assertEquals(categorySerializer.Meta.fields,['id', 'name'])
		self.assertEquals(categorySerializer.Meta.model, Category)


	def testProductSerializer(self):
		data = {'email':'here_is_johnny@gmail.com', 'password':'john'}
		productSerializer = ProductSerializer(data = data)

		#Cheсking the `fields` and `model` in currencySerializer
		self.assertEquals(productSerializer.Meta.fields,['id', 'name', 'category', 'description','currency', 'cost', 'image'])
		self.assertEquals(productSerializer.Meta.model, Product)


	def testTestimonialSerializer(self):
		testimonialSerializer = TestimonialSerializer(data = self.user)
		listSerializer = TestimonialSerializer.ListSerializer(self.user)
		createSerializer = TestimonialSerializer.CreateSerializer(self.user)
		fields = ['id', 'product', 'stars_count', 'description', 'user', 'date_creating']

		#Cheсking the `fields` and `model` in testimonialSerializer
		self.assertEquals(testimonialSerializer.Meta.fields,fields)
		self.assertEquals(testimonialSerializer.Meta.model, Testimonial)

		#Cheсking the `fields` and `model` in listSerializer
		self.assertEquals(listSerializer.Meta.fields,fields)
		self.assertEquals(listSerializer.Meta.model, Testimonial)

		#Cheсking the `fields` and `model` in createSerializer
		self.assertEquals(createSerializer.Meta.fields,fields)
		self.assertEquals(createSerializer.Meta.model, Testimonial)


	def testCartSerializer(self):
		cartSerializer = CartSerializer(data = self.user)
		listSerializer = CartSerializer.ListSerializer(self.user)
		createSerializer = CartSerializer.CreateSerializer(self.user)
		fields = ['id', 'product', 'user', 'date_creating']

		#Cheсking the `fields` and `model` in cartSerializer
		self.assertEquals(cartSerializer.Meta.fields,fields)
		self.assertEquals(cartSerializer.Meta.model, Cart)

		#Cheсking the `fields` and `model` in listSerializer
		self.assertEquals(listSerializer.Meta.fields,fields)
		self.assertEquals(listSerializer.Meta.model, Cart)

		#Cheсking the `fields` and `model` in createSerializer
		self.assertEquals(createSerializer.Meta.fields,fields)
		self.assertEquals(createSerializer.Meta.model, Cart)


	def testOrderSerializer(self):
		orderSerializer = OrderSerializer(data = self.user)
		fields = ['id', 'user', 'hash_code', 'url', 'order_code', 'order_cost', 'paid', 'date_creating']

		#Cheсking the `fields` and `model` in orderSerializer
		self.assertEquals(OrderSerializer.Meta.fields,fields)
		self.assertEquals(OrderSerializer.Meta.model, Order)


	def testGroupSerializer(self):
		groupSerializer = GroupSerializer(data = self.user)
		fields = ['id', 'user', 'product', 'date_creating']

		#Cheсking the `fields` and `model` in groupSerializer
		self.assertEquals(groupSerializer.Meta.fields,fields)
		self.assertEquals(groupSerializer.Meta.model, Group)