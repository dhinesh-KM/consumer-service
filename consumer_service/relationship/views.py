from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializer import *
from .dboperations import *
from common_utils.authentication import Jwt_Authentication
from common_utils.decorator import validate_payload

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
        url_name = request.resolver_match.url_name
        if url_name == 'relationships_bytag':
            instance = get_relationships(self.request.con['coffer_id'], tag = kwargs['tag'])
        
        elif url_name == 'all_relationships':
            instance = get_relationships(self.request.con['coffer_id'])
            
        elif url_name == 'get_consumers':
            instance = get_consumer(request.decode['coffer_id'])
            serializer = GetConSerializer(instance, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        else:
            data = get_relationships(self.request.con['coffer_id'], action='count')
            return Response({'counts':data}, status=status.HTTP_200_OK)
            
        serializer = SpecRelSerializer(instance, many=True, context={ 'con':self.request.con['coffer_id']} )
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        
