from django.urls import path

from . import views
from rest_framework.authtoken import views as auth_token_view

urlpatterns = [
    path('authenticate', views.login_attempt, name='Login'),
    path('me', views.get_me, name='Get Me'),
    path('logout', views.logout_attempt, name='Log out'),
    path('register', views.register, name='Register'),
    path('api-token-auth', auth_token_view.obtain_auth_token)
]

