from django.urls import path
from . import views 


urlpatterns = [
	path('products/<str:category_name>/', views.AllProductsAPIView.as_view(), name = 'shop-products'),
	path('product/<int:id>/', views.CurrentProductRetrieveAPIView.as_view(), name = 'shop-product'),

	path('product/testimonials/<int:product_id>/', views.TestimonialsListCreateAPIView.as_view(), name = 'shop-product-testimonials'),
	path('product/testimonials/<int:product_id>/create/', views.TestimonialsListCreateAPIView.as_view(), name = 'shop-product-testimonials-create'),

	path('cart/<int:user_id>/', views.CartListCreateAPIView.as_view(), name = 'shop-cart'),
	path('cart/<int:user_id>/create/', views.CartListCreateAPIView.as_view(), name = 'shop-cart-create'),
	path('cart/<int:user_id>/<int:product_id>/delete/', views.CartListCreateAPIView.as_view(), name = 'shop-products-delete'),

	path('cart/payment/<int:user_id>/', views.OrderListCreateViewSet.as_view({'get':'list'}), name = 'shop-cart-payment'),
	path('cart/payment/<int:user_id>/create/', views.OrderListCreateViewSet.as_view({'post':'create'}), name = 'shop-cart-payment-create'),
	path('cart/payment/<str:hash_code>/confirm/', views.OrderListCreateViewSet.as_view({'post':'confirm'}), name = 'shop-cart-payment-confirm'),
	path('cart/payment/<str:hash_code>/delete/', views.OrderListCreateViewSet.as_view({'delete':'delete'}), name = 'shop-cart-payment-delete')
]