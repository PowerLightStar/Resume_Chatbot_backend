from django.urls import path
from .views import Signin, Signup, Logout

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('signin/', Signin, name="signin"),
    path('signup/', Signup, name='signup'),
    path('logout', Logout, name="logout"),
    
    path('token/', TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name = "token_refresh"),
    
]
