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

		self.category = Category.objects.create(name = 'All')
		self.currency = Currency.objects.create(name = 'BTC', system_id = 11)
		self.product = Product.objects.create(id = 1000, name = 'Strawberry', description = 'It is pretty delicious', category = self.category, currency = self.currency, cost = 0.002)
		self.testimonial = Testimonial.objects.create(id = 1000, product = self.product, stars_count = 3, description = 'The description of this product didnt lie', user = self.user)
		self.cart = Cart.objects.create(id = 1000, user = self.user, product = self.product)
		self.order = Order.objects.create(id = 1000, user = self.user, hash_code = '23rfkirjdjgjodr', url = '232//', order_code = 232322, order_cost = 0.002)
		self.group = Group.objects.create(id = 1000, user = self.user, product = self.product, order = self.order)


	#Test AllProductsAPIView
	def testProducts(self):
		url = reverse('shop-products',args = [self.category.name])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test CurrentProductRetrieveAPIView
	def testProduct(self):
		url = reverse('shop-product',args = [self.product.id])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test TestimonialsListCreateAPIView - get method
	def testProductTestimonials(self):
		url = reverse('shop-product-testimonials',args = [self.product.id])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test TestimonialsListCreateAPIView - post method
	def testProductTestimonialsCreate(self):
		url = reverse('shop-product-testimonials-create',args = [self.product.id])
		data = {'stars_count':5, 'description':'Nice','user':self.user.id}
		res = self.client.post(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)


	#Test CartListCreateAPIView - get method
	def testShopCart(self):
		url = reverse('shop-cart',args = [self.user.id])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test CartListCreateAPIView - post method
	def testShopCartCreate(self):
		url = reverse('shop-cart-create',args = [self.user.id])
		data = {'product':self.product.id}
		res = self.client.post(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)


	#Test CartListCreateAPIView - delete method
	def testShopCartDelete(self):
		url = reverse('shop-products-delete',args = [self.user.id, self.product.id])
		res = self.client.delete(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test OrderListCreateViewSet - list method
	def testShopCartPayment(self):
		url = reverse('shop-cart-payment',args = [self.user.id])
		res = self.client.get(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test OrderListCreateViewSet - post:create method
	def testShopCartPaymentCreate(self):
		url = reverse('shop-cart-payment-create',args = [self.user.id])
		data = {'amount':0.002, 'products_id':[self.product.id]}
		res = self.client.post(url, data, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test OrderListCreateViewSet - post:confirm method
	def testShopCartPaymentConfirm(self):
		url = reverse('shop-cart-payment-confirm',args = [self.order.hash_code])
		res = self.client.post(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)


	#Test OrderListCreateViewSet - delete method
	def testShopCartPaymentDelete(self):
		url = reverse('shop-cart-payment-delete',args = [self.order.hash_code])
		res = self.client.delete(url, format = 'json')
		self.assertEquals(res.status_code, status.HTTP_200_OK)