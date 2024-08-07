from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, permissions
from bson import ObjectId
from .serializer import *
from .dboperations import *
from rest_framework.permissions import IsAuthenticated
from common_utils.authentication import Jwt_Authentication


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        return consumer_create(data)

    def create(self, request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)
        response.data = {"msg": "Consumer created successfully"}
        return response


class Login(APIView):

    def post(self, request, format=None) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = consumer_login(serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)


class citizenship(APIView):
    authentication_classes = [Jwt_Authentication]

    def post(self, request, format=None) -> Response:
        serializer = CitizenshipSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = consumer_citizenship(serializer.validated_data, 'create', request.con)
        return Response(data, status=status.HTTP_200_OK)
     
    def patch(self, request, *args, **kwargs) -> Response:
        serializer = CitizenshipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            data = consumer_citizenship(serializer.validated_data, 'update', request.con, kwargs['cat'] )
        return Response(data, status=status.HTTP_200_OK)
    
    def get(self, request, **kwargs) -> Response:
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
    
    
        
    def delete(self, request, **kwargs) -> Response:
        data = consumer_citizenship( action = 'delete', con =  request.con, citizen=kwargs['cat'] )
        return Response(data, status=status.HTTP_200_OK)
        
