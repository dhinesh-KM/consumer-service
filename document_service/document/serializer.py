from .models import IdentityDocument
from rest_framework import serializers

class IdentityDocSerializer(serializers.Serializer): 
    category = serializers.CharField() 
    doctype = serializers.CharField 
    docid = serializers.CharField 
    content_type = serializers.CharField 
    filename = serializers.CharField   
    filesize = serializers.IntegerField()
    created = serializers.CharField()
    erification_status = serializers.CharField()
    validity_status = serializers.CharField()
    tags =  serializers.ListField(child=serializers.CharField())
    expiration_date = serializers.CharField()
    country = serializers.CharField
    id = serializers.CharField()
    url = serializers.CharField
    