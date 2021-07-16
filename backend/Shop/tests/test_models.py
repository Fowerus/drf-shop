import jwt

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from Shop.models import *



class TestShopModels(APITestCase):

	def setUp(self):
		self.user = get_user_model()(id = 1000, first_name = "John", last_name = "Smith", email = "here_is_johnny@gmail.com")
		self.user.set_password("john")
		self.user.save()

		self.category = Category.objects.create(name = 'All')
		self.currency = Currency.objects.create(name = 'BTC', system_id = 11)
		self.product = Product.objects.create(name = 'Strawberry', description = 'It is pretty delicious', category = self.category, currency = self.currency, cost = 0.002)
		self.testimonial = Testimonial.objects.create(product = self.product, stars_count = 3, description = 'The description of this product didnt lie', user = self.user)
		self.cart = Cart.objects.create(user = self.user, product = self.product)
		self.order = Order.objects.create(user = self.user, hash_code = '23rfkirjdjgjodr', url = '232//', order_code = 232322, order_cost = 0.002)
		self.group = Group.objects.create(user = self.user, product = self.product, order = self.order)


	def testCategory(self):
		#Checking model fields
		#name
		self.assertEquals(self.category._meta.get_field('name').verbose_name, 'Name')
		self.assertEquals(self.category._meta.get_field('name').max_length, 30)

		#date_creating
		self.assertEquals(self.category._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.category._meta.get_field('date_creating').auto_now_add)

		#Checking meta-class
		self.assertEquals(self.category._meta.verbose_name_plural, 'Categories')
		self.assertEquals(self.category._meta.verbose_name, 'Category')
		self.assertEquals(self.category._meta.ordering, ['-date_creating'])


	def testCurrency(self):
		#Checking model fields
		#name
		self.assertEquals(self.currency._meta.get_field('name').verbose_name, 'Name')
		self.assertEquals(self.currency._meta.get_field('name').max_length, 10)

		#system_id
		self.assertEquals(self.currency._meta.get_field('system_id').verbose_name, 'Id')

		#date_creating
		self.assertEquals(self.currency._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.currency._meta.get_field('date_creating').auto_now_add)

		#Checking meta-class
		self.assertEquals(self.currency._meta.verbose_name_plural, 'Currencies')
		self.assertEquals(self.currency._meta.verbose_name, 'Currency')
		self.assertEquals(self.currency._meta.ordering, ['-date_creating'])


	def testProduct(self):
		#Checking model fields
		#name
		self.assertEquals(self.product._meta.get_field('name').verbose_name, 'Name')
		self.assertEquals(self.product._meta.get_field('name').max_length, 200)

		#description
		self.assertEquals(self.product._meta.get_field('description').verbose_name, 'Description')
		self.assertEquals(self.product._meta.get_field('description').max_length, 1000)

		#image
		self.assertEquals(self.product._meta.get_field('image').verbose_name, 'Image')
		self.assertEquals(self.product._meta.get_field('image').upload_to, './static/Shop/images')
		self.assertEquals(self.product._meta.get_field('image').default, '../static/Shop/images/default-product-image.jpg')
		self.assertEquals(self.product._meta.get_field('image').size, [225,225])

		#category
		self.assertTrue(isinstance(self.product.category, Category))

		#currency
		self.assertTrue(isinstance(self.product.currency, Currency))

		#cost
		self.assertEquals(self.product._meta.get_field('cost').verbose_name, 'Cost')

		#date_creating
		self.assertEquals(self.product._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.product._meta.get_field('date_creating').auto_now_add)

		#Checking meta-class
		self.assertEquals(self.product._meta.verbose_name_plural, 'Products')
		self.assertEquals(self.product._meta.verbose_name, 'Product')
		self.assertEquals(self.product._meta.ordering, ['-date_creating'])


	def testTestimonial(self):
		#Checking model fields
		#product
		self.assertTrue(isinstance(self.testimonial.product, Product))

		#stars_count
		self.assertEquals(self.testimonial._meta.get_field('stars_count').verbose_name, 'Stars')

		#description
		self.assertEquals(self.testimonial._meta.get_field('description').verbose_name, 'Description')
		self.assertEquals(self.testimonial._meta.get_field('description').max_length, 500)

		#user
		self.assertTrue(isinstance(self.testimonial.user, User))

		#date_creating
		self.assertEquals(self.testimonial._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.testimonial._meta.get_field('date_creating').auto_now_add)

		#Checking meta-class
		self.assertEquals(self.testimonial._meta.verbose_name_plural, 'Testimonials')
		self.assertEquals(self.testimonial._meta.verbose_name, 'Testimonial')
		self.assertEquals(self.testimonial._meta.ordering, ['-date_creating'])


	def testCart(self):
		#Checking model fields
		#user
		self.assertTrue(isinstance(self.cart.user, User))

		#product
		self.assertTrue(isinstance(self.cart.product, Product))

		#in_order
		self.assertFalse(self.cart._meta.get_field('in_order').default)

		#date_creating
		self.assertEquals(self.cart._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.cart._meta.get_field('date_creating').auto_now_add)

		#Checking meta-class
		self.assertEquals(self.cart._meta.verbose_name_plural, 'Carts products')
		self.assertEquals(self.cart._meta.verbose_name, 'Carts product')
		self.assertEquals(self.cart._meta.ordering, ['-date_creating'])


	def testOrder(self):
		#Checking model fields
		#user
		self.assertTrue(isinstance(self.order.user, User))

		#hash_code
		self.assertEquals(self.order._meta.get_field('hash_code').verbose_name, 'hash_code')
		self.assertEquals(self.order._meta.get_field('hash_code').max_length, 70)

		#url
		self.assertEquals(self.order._meta.get_field('url').verbose_name, 'url')
		self.assertEquals(self.order._meta.get_field('url').max_length, 200)

		#order_cost
		self.assertEquals(self.order._meta.get_field('order_cost').verbose_name, 'Cost')

		#paid
		self.assertFalse(self.order._meta.get_field('paid').default)

		#date_creating
		self.assertEquals(self.order._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.order._meta.get_field('date_creating').auto_now)

		#Checking meta-class
		self.assertEquals(self.order._meta.verbose_name_plural, 'Orders')
		self.assertEquals(self.order._meta.verbose_name, 'Order')
		self.assertEquals(self.order._meta.ordering, ['-date_creating'])


	def testGroup(self):
		#Checking model fields
		#user
		self.assertTrue(isinstance(self.group.user, User))

		#product
		self.assertTrue(isinstance(self.group.product, Product))

		#product
		self.assertTrue(isinstance(self.group.order, Order))

		#date_creating
		self.assertEquals(self.group._meta.get_field('date_creating').verbose_name, 'Date')
		self.assertTrue(self.group._meta.get_field('date_creating').auto_now)

		#Checking meta-class
		self.assertEquals(self.group._meta.verbose_name_plural, 'Groups')
		self.assertEquals(self.group._meta.verbose_name, 'Group')
		self.assertEquals(self.group._meta.ordering, ['-date_creating'])