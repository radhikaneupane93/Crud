from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Router for LoginViewSet
router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')

app_name = "demo"

urlpatterns = [  
    path('', include(router.urls)),
    path('form/', form,name="form"),
    # User-related endpoints
    path('user/', UserApiView.as_view(), name='user-list-create'),  
    path('user/<str:email>/', UserApiView.as_view(), name='user-detail'),  
]
