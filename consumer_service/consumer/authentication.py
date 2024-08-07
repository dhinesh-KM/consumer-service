from rest_framework.authentication import BaseAuthentication
from consumer_service.custom_exceptions import Custom_Error
from consumer.utils import consumer_by_cofferid
from rest_framework import status
from django.conf import settings
from datetime import datetime
import jwt


class Jwt_Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise Custom_Error("Unauthorized", status.HTTP_401_UNAUTHORIZED)

        try:
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            
        except:
            if jwt.ExpiredSignatureError:
                raise Custom_Error("Token expired.", status.HTTP_400_BAD_REQUEST)
                
        con = consumer_by_cofferid(decode['coffer_id'])
        request.con = con
        request.decode = decode
        return (con, decode)
