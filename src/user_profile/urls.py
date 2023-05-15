from django.urls import path
from user_profile.views import login_user
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logut_user/', logout_user, name='logout'),
    path('register_user/', register_user, name='register_user'),
    path('profile/', profile, name= 'profile'),
    path('change_profile_picture/', change_profile_picture, name= 'change_profile_picture'),
    path('user_notifications/)', user_notifications, name='user_notifications'),
]

