import uuid

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import *
from .serializers import *
from .merchant import paykassa




class AllProductsAPIView(APIView):
	serializer_class = ProductSerializer

	def get(self, requests, category_name):
		try:
			current_category = Category.objects.get(name = category_name)
			products = current_category.categories_products.all()
		except:
			return Response(status = status.HTTP_400_BAD_REQUEST)

		serializer = self.serializer_class(products, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)



class CurrentProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'id'



class TestimonialsListCreateAPIView(APIView):
	serializer_class = TestimonialSerializer

	def get(self, requests, product_id):
		try:
			current_product = Product.objects.get(id = product_id)
		except:
			return Response(status = status.HTTP_400_BAD_REQUEST)

		serializer = self.serializer_class.ListSerializer(current_product.products_testimonials, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)


	def post(self, requests, product_id):
		requests.data.update({'product':product_id})
		serializer = self.serializer_class.CreateSerializer(data = requests.data)

		if serializer.is_valid():
			serializer.save()
			serializer = serializer.get_current_testimonial(serializer.data['id'])
			return Response(self.serializer_class.ListSerializer(serializer).data, status = status.HTTP_201_CREATED)

		return Response(status = status.HTTP_400_BAD_REQUEST)



class CartListCreateAPIView(APIView):
	serializer_class = CartSerializer

	def get(self, requests, user_id):
		try:
			current_user = get_user_model().objects.get(id = user_id)
		except:
			return Response(status = status.HTTP_400_BAD_REQUEST)

		serializer = self.serializer_class.ListSerializer(current_user.user_cart.all().filter(in_order = False), many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)


	def post(self, requests, user_id):
		requests.data.update({'user':user_id})
		serializer = self.serializer_class.CreateSerializer(data = requests.data)

		if serializer.is_valid():
			serializer.save()
			serializer = serializer.get_current_product(serializer.data['id'])
			return Response(self.serializer_class.ListSerializer(serializer).data, status = status.HTTP_201_CREATED)

		return Response(status = status.HTTP_400_BAD_REQUEST)


	def delete(self, requests, user_id, product_id):
		product = Cart.objects.filter(user = user_id).get(product = product_id)
		product.delete()

		return self.get(requests, user_id)



class OrderListCreateViewSet(viewsets.ViewSet):
	serializer_class = OrderSerializer

	def list(self, requests, user_id):
		serializer_data = {}
		orders_no_paid = Order.objects.filter(user = user_id).filter(paid = False)

		if orders_no_paid:
			serializer = self.serializer_class(orders_no_paid, many = True)
			serializer_data_no_paid = serializer.data

			for i in range(len(serializer_data_no_paid)):
				serializer_data_no_paid[i].update({'products':GroupSerializer(orders_no_paid[i].groups_order.all(),many = True).data})

			serializer_data.update({'no_paid':serializer_data_no_paid})

		orders_paid = Order.objects.filter(user = user_id).filter(paid = True)

		if orders_paid:
			serializer = self.serializer_class(orders_paid, many = True)
			serializer_data_paid = serializer.data

			for i in range(len(serializer_data_paid)):
				serializer_data_paid[i].update({'products':GroupSerializer(orders_no_paid[i].groups_order.all(),many = True).data})

			serializer_data.update({'paid':serializer_data_paid})

		return Response(serializer_data, status = status.HTTP_200_OK)


	def create(self, requests, user_id):
		try:
			order_code = int(str(uuid.uuid1().int)[:10])
			create_order = paykassa.sci_create_order(float(requests.data['amount']), order_code, comment = '')

			if 'error' in create_order and create_order['error'] == False:
				order = Order.objects.create(
					user = User.objects.get(id = user_id), 
					hash_code = create_order['data']['params']['hash'],
					url = create_order['data']['url'],
					order_code = order_code,
					order_cost = float(requests.data['amount']))

				for i in requests.data['products_id']:
					Group.objects.create(user = User.objects.get(id = user_id), product = Product.objects.get(id = int(i)), order = order)

				for i in get_user_model().objects.get(id = user_id).user_cart.all():
					i.in_order = True
					i.save()

				return self.list(requests, user_id)

			return Response(status = status.HTTP_400_BAD_REQUEST)

		except:
			return Response(status = status.HTTP_404_NOT_FOUND)


	def confirm(self, requests, hash_code):
		try:
			confirm_order = paykassa.sci_confirm_order(hash_code)

			if 'error' in confirm_order and confirm_order['error'] == False:
				order = Order.objects.get(hash_code = hash_code)
				order.paid = True
				order.save()
				return self.list(requests, order.user.id)

			return Response({'error': 'Order not confirmed'}, status = status.HTTP_200_OK)

		except:
			return Response(status = status.HTTP_404_NOT_FOUND)


	def delete(self, requests, hash_code):
		try:
			order = Order.objects.get(hash_code = hash_code)
			order.delete()
			return self.list(requests, order.user.id)

		except:
			return Response(status = status.HTTP_404_NOT_FOUND)