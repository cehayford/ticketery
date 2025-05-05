from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_sso.views import obtain_session_token, obtain_authorization_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('bkg/', include('bookings.urls')),
    re_path(r'^session/', obtain_session_token),
    re_path(r'^authorize/', obtain_authorization_token)
]

