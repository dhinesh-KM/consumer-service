from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializer import *
from .dboperations import *
from common_utils.authentication import Jwt_Authentication
from common_utils.validator import validate_payload

class SpecRelView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    
    def get_serializer_class(self):
        
        path = self.request.path.split('/')[-1]
        
        if self.request.method == 'POST':
            if path == 'request':
                return SpecRelReqSerializer
            
            if path == 'accept':
                return SpecRelAcpSerializer
            
        return GetConSerializer
    
    def get(self, request, *args, **kwargs):
        instance = get_consumer(request.decode['coffer_id'])
        serializer = GetConSerializer(instance, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    @validate_payload
    def post(self, request, *args, **kwargs):
        if self.get_serializer_class() == SpecRelReqSerializer:
            data = request_consumer(self.payload, request.con)
            return Response(data, status=status.HTTP_201_CREATED)
        
        else:        
            data = accept_consumer(self.payload, request.con, kwargs['rel_id'])
            return Response(data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        instances = get_relationships(self.request.con['coffer_id'])
        print(instances , len(instances))
        serializer = SpecRelSerializer(instances,  context={ 'con':self.request.con['coffer_id']}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
