from django.urls import path
from .views import GoogleLogin,UserMe

urlpatterns = [
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('users/me/', UserMe.as_view(), name='user_detail')
]