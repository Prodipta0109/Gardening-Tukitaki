from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logut_user/', logout_user, name='logout'),
    path('register_user/', register_user, name='register_user')
]

