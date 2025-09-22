from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('register-jwt/', views.register_user_with_jwt),
    path('me/', views.user_detail),

    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view())
]
