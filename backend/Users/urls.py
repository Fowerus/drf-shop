from django.urls import path
from . import views 


urlpatterns = [
	path('registration/', views.UserRegistrationAPIView.as_view()),
	path('login/', views.UserLoginAPIView.as_view()),
	path('update/<int:user_id>/', views.UserRetrieveUpdateAPIView.as_view())
]