from rest_framework.authentication import BaseAuthentication
from .custom_exceptions import Custom_Error
<<<<<<< HEAD
from rest_framework import status
from django.conf import settings
import jwt,requests
=======
from consumer.utils import consumer_by_cofferid
from rest_framework import status
from django.conf import settings
import jwt
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201


class Jwt_Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise Custom_Error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
        try:
<<<<<<< HEAD
            url = f'{settings.CONSUMER_SERVICE}/api/v1/consumer/data'
            headers = {'Authorization': token}
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            con = requests.get(url, headers=headers)
            request.con = con.json()['data']
=======
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            con = consumer_by_cofferid(decode['coffer_id'])
            request.con = con
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
            request.decode = decode
            return (con, decode)
        
        except jwt.exceptions.ExpiredSignatureError:
            raise Custom_Error("Token expired.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
<<<<<<< HEAD
            raise Custom_Error("Invalid token..", status.HTTP_400_BAD_REQUEST)
=======
            raise Custom_Error("Invalid token.", status.HTTP_400_BAD_REQUEST)
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
        except jwt.exceptions.DecodeError:
            raise Custom_Error("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise Custom_Error(f"{str(e)}", status.HTTP_400_BAD_REQUEST)

                
        
