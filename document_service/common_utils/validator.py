from .utils import con_citz
from .custom_exceptions import Custom_Error
from rest_framework import status

def validate_payload(func):
    def wrapper(self, request, *args, **kwargs):
        print("***************",request.data, len(request.data))
        if len(request.data) > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.payload = serializer.validated_data
        
        if kwargs['cat'] not in con_citz(request.con['citizen']):
            raise Custom_Error('Citizenship not found', status.HTTP_404_NOT_FOUND)
        
        

        return func(self, request, *args, **kwargs)
    return wrapper



        