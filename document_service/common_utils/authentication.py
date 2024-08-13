from rest_framework.authentication import BaseAuthentication
from .custom_exceptions import Custom_Error
from rest_framework import status
from django.conf import settings
import jwt,requests
from rest_framework import status
from django.conf import settings
import jwt


class Jwt_Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("Authorization")
        
        if not token:
            raise Custom_Error("Unauthorized", status.HTTP_401_UNAUTHORIZED)
        
        try:
            url = f'{settings.CONSUMER_SERVICE}/api/v1/consumer/data'
            headers = {'Authorization': token}
            decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
            con = requests.get(url, headers=headers)
            request.con = con.json()['data']
            request.decode = decode
            return (con, decode)
        
        except jwt.exceptions.ExpiredSignatureError:
            raise Custom_Error("Token expired.", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            raise Custom_Error("Invalid token..", status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            raise Custom_Error("Invalid token.", status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            print('-----> please start the consumer_service <-------')
            raise Custom_Error('something went wrong, please try again', status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            raise Custom_Error(f"{str(e)}", status.HTTP_400_BAD_REQUEST)
        

                
        
