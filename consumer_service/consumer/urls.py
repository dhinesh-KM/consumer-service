from .views import *
from django.urls import path

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('citizenship',Citizenship.as_view(),name='CR_citizenship'),
    path('citizenship/<str:cat>', Citizenship.as_view(),name='RUD_citzenship'),
<<<<<<< HEAD
    path('citizenship/<str:country>/affiliations', Citizenship.as_view(), name='get_affiliations'),
    path('data', GetConsumer.as_view(), name='get_consumer')
=======
    path('citizenship/<str:country>/affiliations', Citizenship.as_view(), name='get_affiliations')
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
] 
