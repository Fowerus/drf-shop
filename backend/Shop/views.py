from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import *
from .serializers import *




class AllProductsAPIView(APIView):
	serializer_class = AllProductsSerializer

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
		serializer = self.serializer_class(current_product.products_testimonials, many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)
