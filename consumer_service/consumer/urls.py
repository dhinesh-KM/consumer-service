from .views import *
from django.urls import path

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('citizenship',citizenship.as_view(),name='create_citizenship'),
    path('citizenship/<str:cat>', citizenship.as_view(),name='update_citozenship'),
    path('citizenship/<str:country>/affiliations', citizenship.as_view(), name='get_affiliations')
] 
