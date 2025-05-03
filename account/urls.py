from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', UserView.as_view(), name='user_list'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/create/', CreateUserInfoView.as_view(), name='create_user_information'),
    path('user/<str:pk>/update/', UpdateUserInfoView.as_view(), name='update_user_information'),
    path('activate/<str:uidb64>/<str:token>', sso_authentication.as_view(), name='sso_activate'),
path('confirm/<uidb64>/<token>', sso_authentication_confirm.as_view(), name='sso_activation_confirm'),
]