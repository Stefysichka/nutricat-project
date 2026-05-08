from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),                              
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cats/', views.get_cats, name='get_cats'),
    path('cats/<int:pk>/', views.get_cat_detail, name='get_cat_detail'),
    path('cats/<int:pk>/photo/', views.update_cat_photo, name='update_cat_photo'),                                   
    path('cats/<int:pk>/generate-ration/', views.generate_cat_ration, name='generate_cat_ration'),
    path('chat/', views.cat_chat_endpoint, name='cat_chat'),
]

