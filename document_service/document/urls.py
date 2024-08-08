from .views import *
from django.urls import path

urlpatterns =[
    path('identity/<str:cat>', IdocView.as_view(), name='Idoc_ops')
]