from django.urls import path

from .views import *

urlpatterns =[
    path('sell_post/', sell_post, name='sell_post')
]