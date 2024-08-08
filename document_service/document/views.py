<<<<<<< HEAD
from rest_framework import generics
from .serializer import IdentityDocSerializer
from common_utils.validator import validate_payload
from common_utils.authentication import Jwt_Authentication

class IdocView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    serializer_class = IdentityDocSerializer
    
    @validate_payload
    def post(self, request, *args, **kwargs):
        print("****")
        print(self.payload)
        pass
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
