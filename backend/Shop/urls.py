from django.urls import path
from . import views 


urlpatterns = [
	path('products/<str:category_name>/', views.AllProductsAPIView.as_view()),
	path('product/<int:id>/', views.CurrentProductRetrieveAPIView.as_view()),
	path('product/testimonial/<int:product_id>/', views.TestimonialsListCreateAPIView.as_view())
]