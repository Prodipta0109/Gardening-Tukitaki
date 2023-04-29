from django.urls import path

from .views import *

urlpatterns =[
    path('gardening_calculator/', gardening_calculator, name='gardening_calculator')
]