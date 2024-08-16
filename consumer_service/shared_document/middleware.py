from .models import SharedDocument
from rest_framework import status
from common_utils.custom_exceptions import CustomError
from django.conf import settings
import requests



def miss_Ids(self, request):
    url = f'{settings.DOCUMENT_SERVICE}/api/v1/consumer/data'
    headers = {'Authorization': token}
    decode = jwt.decode(token.split(' ')[1], settings.SECRET_KEY, algorithms=["HS256"])
    con = requests.get(url, headers=headers)
    request.con = con.json()['data']
    