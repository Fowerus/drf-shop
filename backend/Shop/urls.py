from django.urls import path
from . import views 


urlpatterns = [
	path('products/<str:category_name>/', views.AllProductsAPIView.as_view()),
	path('product/<int:id>/', views.CurrentProductRetrieveAPIView.as_view()),

	path('product/testimonials/<int:product_id>/', views.TestimonialsListCreateAPIView.as_view()),
	path('product/testimonials/<int:product_id>/create/', views.TestimonialsListCreateAPIView.as_view()),

	path('cart/<int:user_id>/', views.CartListCreateAPIView.as_view()),
	path('cart/<int:user_id>/create/', views.CartListCreateAPIView.as_view()),

	path('cart/payment/<int:user_id>/', views.OrderListCreateAPIView.as_view())
]