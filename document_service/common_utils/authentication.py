from rest_framework.authentication import BaseAuthentication
from .custom_exceptions import Custom_Error
from consumer.utils import consumer_by_cofferid
from rest_framework import status
from django.conf import settings
import jwt


class Jwt_Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise Custom_Error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
        try:
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            con = consumer_by_cofferid(decode['coffer_id'])
            request.con = con
            request.decode = decode
            return (con, decode)
        
        except jwt.exceptions.ExpiredSignatureError:
            raise Custom_Error("Token expired.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            raise Custom_Error("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            raise Custom_Error("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise Custom_Error(f"{str(e)}", status.HTTP_400_BAD_REQUEST)

                
        
