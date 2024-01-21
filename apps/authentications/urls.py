from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView

from .views import CustomTokenObtainView


urlpatterns = [
    path('auth/', CustomTokenObtainView.as_view(), name='token_authentication'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]