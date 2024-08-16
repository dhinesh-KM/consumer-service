from rest_framework import generics,status
from rest_framework.response import Response
from .serializer import *
from common_utils.validator import validate_payload
from common_utils.authentication import Jwt_Authentication
from .dboperations import *
import datetime

class IdocView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IdocPostSerializer
        
        elif self.request.method == 'PATCH':
            return IdocPatchSerializer

        return IdentityDocSerializer
    
    @validate_payload
    def post(self, request, *args, **kwargs):
        data = idoc_operations(self.payload, 'create', request.con, kwargs)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @validate_payload
    def get(self, request, *args, **kwargs):
        data = None
        if 'action' in list(kwargs.keys()):
            data = idoc_operations( action=kwargs['action'], con=request.con, citz=kwargs)

        elif 'doctype' in list(kwargs.keys()):
            instance = idoc_operations( action='get_one', con=request.con, citz=kwargs)
            serializer = IdentityDocSerializer(instance)
            data = [serializer.data]
            
        elif 'doctype' not in list(kwargs.keys()):
            instance = idoc_operations( action='get_all', con=request.con, citz=kwargs)
            serializer = IdentityDocSerializer(instance, many=True)
            data = serializer.data
            
        return Response({'data': data}, status=status.HTTP_200_OK)
    
    @validate_payload
    def patch(self, request,  *args, **kwargs):
        data = idoc_operations(self.payload, 'update', request.con, kwargs)
        return Response(data, status=status.HTTP_200_OK)
    
    @validate_payload
    def delete(self, request,  *args, **kwargs):
        data = idoc_operations(action='delete', con = request.con, citz = kwargs)
        return Response(data, status=status.HTTP_200_OK)
    
    
class IdocUtilView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    
    def post(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name
        if url_name == 'missing_ids':
            data = getAllDocs(request.data, request.con['coffer_id'])
        if url_name == 'doc_details':
            instances = getAllDocsDetails(request.data)
            serializer = SharedIdentityDocSerializer(instances, many=True)
            data = {'data' : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        data = document_action(kwargs)
        return Response(data, status=status.HTTP_200_OK)
    
           
        


