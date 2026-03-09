from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    # 1. SIGN UP: POST to create a new user
    path('register/', RegisterView.as_view(), name='auth_register'),

    # 2. LOGIN: POST email and password to get 'access' and 'refresh' tokens
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 3. REFRESH: POST the refresh token to get a new access token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]