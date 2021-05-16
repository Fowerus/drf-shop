from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import *
from .serializers import *




class AllProductsAPIView(APIView):
	serializer_class = ProductSerializer

	def get(self, requests, category_name):
		current_category = Category.objects.get(name = category_name)
		products = Product.objects.filter(category = current_category.id)
		serializer = self.serializer_class(products, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)



class CurrentProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = CurrentProductSerializer
	lookup_field = 'id'



class TestimonialsListCreateAPIView(APIView):
	serializer_class = TestimonialSerializer

	def get(self, requests, product_id):
		current_product = Product.objects.get(id = product_id)
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
		current_user = User.objects.get(id = user_id)
		serializer = self.serializer_class.ListSerializer(current_user.user_cart.filter(in_order = False), many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)

	def post(self, requests, user_id):
		requests.data.update({'user':user_id})
		serializer = self.serializer_class.CreateSerializer(data = requests.data)
		if serializer.is_valid():
			serializer.save()

			serializer = serializer.get_current_product(serializer.data['id'])
			return Response(self.serializer_class.ListSerializer(serializer).data, status = status.HTTP_201_CREATED)

		return Response(status = status.HTTP_400_BAD_REQUEST)



class OrderListCreateAPIView(APIView):
	serializer_class = OrderSerializer

	def get(self, requests, user_id):
		orders = Order.objects.filter(user = user_id).filter(paid = False)

		print(orders[0].groups_order)

		return Response(status = status.HTTP_200_OK)

