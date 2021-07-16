from django.db import models
from django_resized import ResizedImageField

from Users.models import *


class Category(models.Model):
	name = models.CharField(max_length = 30, verbose_name = 'Name')
	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'Date')

	def __str__(self):
		return f'{self.name}'


	class Meta:
		verbose_name_plural = 'Categories'
		verbose_name = 'Category'
		ordering = ['-date_creating']



class Currency(models.Model):
	name = models.CharField(max_length = 10, verbose_name = 'Name')
	system_id = models.IntegerField(verbose_name = 'Id')
	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'Date')

	def __str__(self):
		return f'{self.name}'


	class Meta:
		verbose_name_plural	= 'Currencies'
		verbose_name = 'Currency'
		ordering = ['-date_creating']



class Product(models.Model):
	name = models.CharField(max_length = 200, verbose_name = 'Name')
	description	= models.CharField(max_length = 1000, verbose_name = 'Description')
	image = ResizedImageField(size = [225,225], upload_to='./static/Shop/images', default = '../static/Shop/images/default-product-image.jpg', verbose_name = 'Image')
	category = models.ForeignKey(Category, on_delete = models.PROTECT, verbose_name = 'Category', default = 1, related_name = 'categories_products')
	currency = models.ForeignKey(Currency, on_delete = models.CASCADE, verbose_name = 'Currency', default = 1, related_name = 'currency_product')
	cost = models.FloatField(verbose_name = 'Cost')
	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'Date')

	def __str__(self):
		return f'id: {self.id} | category: {self.category} | name: {self.name}'


	class Meta:
		verbose_name_plural = 'Products'
		verbose_name = 'Product'
		ordering = ['-date_creating']



class Testimonial(models.Model):
	product = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = 'Product', related_name = 'products_testimonials')
	stars_count = models.IntegerField(verbose_name = 'Stars')
	description = models.CharField(max_length = 500, verbose_name = 'Description')
	user = models.ForeignKey(User, on_delete = models.PROTECT, verbose_name = 'User', related_name = 'my_testimonials')

	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'Date')

	def __str__(self):
		return f'id : {self.id} | product: {self.product.id} | stars: {self.stars_count} | user: {self.user.id}'


	class Meta:
		verbose_name_plural = 'Testimonials'
		verbose_name = 'Testimonial'
		ordering = ['-date_creating']



class Cart(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Cart', related_name = 'user_cart')
	product	= models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Product', related_name = 'product_buyer')

	in_order = models.BooleanField(default = False)

	date_creating = models.DateTimeField(auto_now_add = True, verbose_name = 'Date')

	def __str__(self):
		return f'user: {self.user.id} | product: {self.product.id}'


	class Meta:
		verbose_name_plural = 'Carts products'
		verbose_name = 'Carts product'
		ordering = ['-date_creating']



class Order(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Orders', related_name = 'user_cart_orders')
	hash_code = models.CharField(max_length = 70, verbose_name = 'hash_code')
	url	= models.CharField(max_length = 200, verbose_name = 'url')
	order_code = models.IntegerField()

	order_cost = models.FloatField(verbose_name = 'Cost')

	paid = models.BooleanField(default = False)
	date_creating = models.DateTimeField(auto_now = True, verbose_name = 'Date')

	def __str__(self):
		return f'id: {self.id} | paid: {self.paid}'


	class Meta:
		verbose_name_plural = 'Orders'
		verbose_name = 'Order'
		ordering = ['-date_creating']



class Group(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Groups', related_name = 'user_cart_groups')
	product	= models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Groups', related_name = 'product_in_groups')
	order = models.ForeignKey(Order, on_delete = models.CASCADE, verbose_name = 'order_id', related_name = 'groups_order')

	date_creating = models.DateTimeField(auto_now = True, verbose_name = 'Date')	

	def __str__(self):
		return f'id: {self.id} | user : {self.user.id} | product: {self.product.id} | order: {self.order.id}'


	class Meta:
		verbose_name_plural = 'Groups'
		verbose_name = 'Group'
		ordering = ['-date_creating']