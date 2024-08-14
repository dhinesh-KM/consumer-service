import requests
from django.conf import settings


def validate_payload(func):
    def wrapper(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.payload = serializer.validated_data
        
        return func(self, request, *args, **kwargs)
    return wrapper
        
        
def check_user_resources(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            url = f'{settings.DOCUMENT_SERVICE}/api/v1/document/identity/{kwargs['cat']}'
            headers = {'Authorization': request.headers.get("Authorization")}
            idoc = requests.get(url, headers=headers)            
            self.idoc = len(idoc.json()['data'])
            
        except Exception as e:
            print(e)
        return func(self, request, *args, **kwargs)
    return wrapper

