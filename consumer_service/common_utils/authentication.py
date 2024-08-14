from rest_framework.authentication import BaseAuthentication
from .custom_exceptions import CustomError
from .utils import consumer_by_cofferid
from rest_framework import status
from django.conf import settings
import jwt


class Jwt_Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise CustomError("Unauthorized", status.HTTP_401_UNAUTHORIZED)
        try:
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            con = consumer_by_cofferid(decode['coffer_id'])
            request.con = con
            request.decode = decode
            return (con, decode)
        
        except jwt.exceptions.ExpiredSignatureError:
            raise CustomError("Token expired.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            raise CustomError("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            raise CustomError("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise CustomError(f"{str(e)}", status.HTTP_400_BAD_REQUEST)

                
        
