from .views import *
from django.urls import path

urlpatterns =[
    path('identity/<str:cat>', IdocView.as_view(), name='CR_idoc'),
    path('identity/<str:cat>/<str:doctype>', IdocView.as_view(), name='RUD_idoc'),
    path('identity/<str:cat>/<str:doctype>/<str:action>', IdocView.as_view(), name='VD_idoc'),
]