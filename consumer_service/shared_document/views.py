
from rest_framework import generics, status
from rest_framework.response import Response
from .models import SharedDocument
from .serializers import SharedDocSerializer
from common_utils.authentication import Jwt_Authentication
from common_utils.decorator import validate_payload
from .middleware import *
from .dboperations import share_docs

class SharedDocumentView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    serializer_class = SharedDocSerializer
    
    @validate_payload
    def post(self, request, *args, **kwargs):
        data = missing_ids(request, kwargs['rel_id'])
        data = share_docs(data = self.payload['data'], cofferid = request.con['coffer_id'], relid = kwargs['rel_id'], action = kwargs['action'], docs = data)
        return Response(data, status = status.HTTP_201_CREATED)
    
    
    def get(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name
        
        if url_name in ['by_me', 'with_me']:
            data = document_details(request, relid = kwargs['rel_id'])
            
        else:
            data = document_action(request, **kwargs)
            
        return Response(data, status = status.HTTP_200_OK)