
from rest_framework import generics, status
from rest_framework.response import Response
from .models import SharedDocument
from common_utils.authentication import Jwt_Authentication

class SharedDocumentView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    
    def post(self, request, *args, **kwargs):
        pass