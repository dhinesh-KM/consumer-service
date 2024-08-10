from .models import IdentityDocument
from rest_framework import serializers,status
from common_utils.utils import doctype_validate
from common_utils.custom_exceptions import Custom_Error
import datetime



class IdentityDocSerializer(serializers.Serializer): 
    category = serializers.CharField(read_only=True) 
    doctype = serializers.CharField()
    docid = serializers.CharField()
    content_type = serializers.CharField(read_only=True)
    filename = serializers.CharField(read_only=True) 
    filesize = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    verification_status = serializers.CharField(read_only=True)
    validity_status = serializers.CharField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    expiration_date = serializers.DateTimeField(required=False, input_formats=['%d-%m-%Y'])
    country = serializers.CharField()
    id = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    file = serializers.FileField(write_only=True)
    
    def validate(self, attrs):
        doctype_validate(attrs['country'], attrs['doctype'], attrs['docid'])
        if attrs['doctype'] in ['passport', 'driver_license']:
            if 'expiration_date' not in list(attrs.keys()):
                raise Custom_Error('Expiration date is required', status.HTTP_400_BAD_REQUEST)
            else:
                if attrs['expiration_date'].replace(tzinfo=None) <= datetime.datetime.today():                    
                    raise Custom_Error('Expiration date should be a future date', status.HTTP_400_BAD_REQUEST)
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created'] = instance.created.strftime('%b-%d-%Y %I:%M:%S %p')
        
        representation['expiration_date'] = instance.created.strftime('%b-%d-%Y %I:%M:%S %p') if representation['expiration_date'] is not None else 'NA'
        return representation
        

    