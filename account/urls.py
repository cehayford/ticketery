from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from .views import *
urlpatterns = [
    path('oauth/', include(oauth2_urls)),
    path('auth/', include('djoser.urls')),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/create/', CreateUserInfoView.as_view(), name='create_user_information'),
    path('user/<str:pk>/update/', UpdateUserInfoView.as_view(), name='update_user_information')
]