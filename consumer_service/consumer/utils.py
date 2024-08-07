from rest_framework.response import Response
from .models import Consumer
from common_utils.custom_exceptions import *


def consumer_by_cofferid(cofferid: str) -> object:
    con = Consumer.objects(coffer_id=cofferid).first()
    if con:
        return con
    raise Not_Found("Consumer not found")


def consumer_find(data: dict) -> dict:

    con = Consumer.objects(__raw__=data).first()
    if con:
        return con
    raise Not_Found("Consumer not found")
