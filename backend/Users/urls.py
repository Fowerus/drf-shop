from django.urls import path
from . import views 


urlpatterns = [
	path('registration/', views.UserRegistrationAPIView.as_view()),
	path('login/', views.UserLoginAPIView.as_view()),
]