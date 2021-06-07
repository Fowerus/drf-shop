from django.urls import path
from . import views 


urlpatterns = [
	path('products/<str:category_name>/', views.AllProductsAPIView.as_view()),
	path('product/<int:id>/', views.CurrentProductRetrieveAPIView.as_view()),

	path('product/testimonials/<int:product_id>/', views.TestimonialsListCreateAPIView.as_view()),
	path('product/testimonials/<int:product_id>/create/', views.TestimonialsListCreateAPIView.as_view()),

	path('cart/<int:user_id>/', views.CartListCreateAPIView.as_view()),
	path('cart/<int:user_id>/create/', views.CartListCreateAPIView.as_view()),
	path('cart/<int:user_id>/<int:product_id>/delete/', views.CartListCreateAPIView.as_view()),

	path('cart/payment/<int:user_id>/', views.OrderListCreateViewSet.as_view({'get':'list'})),
	path('cart/payment/<int:user_id>/create/', views.OrderListCreateViewSet.as_view({'post':'create'})),
	path('cart/payment/<str:hash_code>/confirm/', views.OrderListCreateViewSet.as_view({'post':'confirm'})),
	path('cart/payment/<str:hash_code>/delete/', views.OrderListCreateViewSet.as_view({'delete':'delete'}))
]