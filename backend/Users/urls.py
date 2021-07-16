from django.urls import path
from . import views 


urlpatterns = [
	path('registration/', views.UserRegistrationAPIView.as_view(), name = 'user-registration'),
	path('login/', views.UserLoginAPIView.as_view(), name = 'user-login'),
	path('retrieve/<int:user_id>/', views.UserRetrieveUpdateAPIView.as_view(), name = 'user-retrieve'),
	path('update/<int:user_id>/', views.UserRetrieveUpdateAPIView.as_view(), name = 'user-update'),

	path('check-token/',views.CheckTokenAPIView.as_view(), name = 'user-check-token')
]