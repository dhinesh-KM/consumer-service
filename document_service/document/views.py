from rest_framework import generics,status
from rest_framework.response import Response
from .serializer import IdentityDocSerializer
from common_utils.validator import validate_payload
from common_utils.authentication import Jwt_Authentication
from .dboperations import Idoc_operations

class IdocView(generics.GenericAPIView):
    authentication_classes = [Jwt_Authentication]
    serializer_class = IdentityDocSerializer
    
    @validate_payload
    def post(self, request, *args, **kwargs):
        data = Idoc_operations(self.payload, 'create', request.con, kwargs)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @validate_payload
    def delete(self, request,  *args, **kwargs):
        print(self.payload)
        data = Idoc_operations(con = request.con, citz = kwargs)
        return Response(data, status=status.HTTP_200_OK)


