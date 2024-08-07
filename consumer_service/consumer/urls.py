from .views import *
from django.urls import path

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('citizenship',citizenship.as_view(),name='CR_citizenship'),
    path('citizenship/<str:cat>', citizenship.as_view(),name='RUD_citzenship'),
    path('citizenship/<str:country>/affiliations', citizenship.as_view(), name='get_affiliations')
] 
