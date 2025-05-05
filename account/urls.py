from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', UserView.as_view(), name='user_list'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/create/', CreateUserInfoView.as_view(), name='create_user_information'),
    path('user/<str:pk>/update/', UpdateUserInfoView.as_view(), name='update_user_information'),
    re_path(r'^authorize/$', ObtainAuthorizationTokenView.as_view()),
]