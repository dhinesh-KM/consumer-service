from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, permissions
from bson import ObjectId
from .serializer import *
from .dboperations import *
from rest_framework.permissions import IsAuthenticated
from common_utils.authentication import Jwt_Authentication
from common_utils.validator import validate_payload


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        return consumer_create(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"msg": "Consumer created successfully"}
        return response


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    @validate_payload
    def post(self, request):
        data = consumer_login(self.payload)
        return Response(data, status=status.HTTP_201_CREATED)


class Citizenship(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    serializer_class = CitizenshipSerializer

    @validate_payload
    def post(self, request):
        data = consumer_citizenship(self.data, 'create', request.con)
        return Response(data, status=status.HTTP_200_OK)
    
    @validate_payload
    def patch(self, request, *args, **kwargs):
        data = consumer_citizenship(self.payload, 'update', request.con, kwargs['cat'] )
        return Response(data, status=status.HTTP_200_OK)
    
    def get(self, request, **kwargs):
        
        if len(kwargs.keys()) == 0:
            serializer = CitizenshipSerializer(request.con.citizen, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        for key,value in kwargs.items():
            if key == 'cat':
                data = consumer_citizenship(action = 'view', con =  request.con, citizen=value )
                return Response(data, status=status.HTTP_200_OK)
            if key == 'country':
                data = consumer_affiliations( value )
                return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, **kwargs):
        data = consumer_citizenship( action = 'delete', con =  request.con, citizen=kwargs['cat'] )
        return Response(data, status=status.HTTP_200_OK)
        
