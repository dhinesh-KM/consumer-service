from .models import IdentityDocument
from rest_framework import serializers

class IdentityDocSerializer(serializers.Serializer): 
<<<<<<< HEAD
    category = serializers.CharField(read_only=True) 
    doctype = serializers.CharField()
    docid = serializers.CharField()
    content_type = serializers.CharField(read_only=True)
    filename = serializers.CharField(read_only=True) 
    filesize = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    verification_status = serializers.CharField(read_only=True)
    validity_status = serializers.CharField(read_only=True)
    tags =  serializers.ListField(child=serializers.CharField())
    expiration_date = serializers.DateTimeField(read_only=True)
    country = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    file = serializers.FileField(write_only=True)
    
    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
=======
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
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
    