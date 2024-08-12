from .models import IdentityDocument
from rest_framework import serializers,status
from common_utils.utils import doctype_validate
from common_utils.custom_exceptions import Custom_Error
import datetime

class IdocPostSerializer(serializers.Serializer): 
    doctype = serializers.CharField()
    docid = serializers.CharField()
    file = serializers.FileField(write_only=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    expiration_date = serializers.DateTimeField(required=False, input_formats=['%d-%m-%Y'])
    
    def validate(self, attrs):
        kwargs = self.context.get('kwargs')
        doctype_validate(kwargs['country'] , attrs['doctype'], attrs['docid'])
        
        if attrs['doctype'] not in ['passport', 'driver_license'] and 'expiration_date' in attrs:
            del attrs['expiration_date']
            
        if attrs['doctype'] in ['passport', 'driver_license']:
            if 'expiration_date' not in attrs:
                raise Custom_Error('Expiration date is required', status.HTTP_400_BAD_REQUEST)

            if attrs['expiration_date'].replace(tzinfo=None) <= datetime.datetime.today():                    
                raise Custom_Error('Expiration date should be a future date', status.HTTP_400_BAD_REQUEST)
        
        return attrs
                
                
class IdocPatchSerializer(serializers.Serializer): 
    docid = serializers.CharField(required=False)
    expiration_date = serializers.DateTimeField(required=False, input_formats=['%d-%m-%Y'])
    
    def validate(self, attrs):
        kwargs = self.context.get('kwargs')
        if kwargs['doctype'] not in ['passport', 'driver_license'] and 'expiration_date' in attrs:
                del attrs['expiration_date']
        
        if 'expiration_date' in attrs:
            if attrs['expiration_date'].replace(tzinfo=None) <= datetime.datetime.today():                    
                raise Custom_Error('Expiration date should be a future date', status.HTTP_400_BAD_REQUEST)
        return attrs

class IdentityDocSerializer(serializers.Serializer): 
    category = serializers.CharField(required=False) 
    doctype = serializers.CharField(required=False)
    docid = serializers.CharField(required=False)
    content_type = serializers.CharField(required=False)
    filename = serializers.CharField(required=False) 
    filesize = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    verification_status = serializers.CharField(required=False)
    validity_status = serializers.CharField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    expiration_date = serializers.DateTimeField(required=False)
    country = serializers.CharField(required=False)
    id = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created'] = instance.created.strftime('%b-%d-%Y %I:%M:%S %p')
        
        representation['expiration_date'] = instance.created.strftime('%b-%d-%Y %I:%M:%S %p') if representation['expiration_date'] is not None else 'NA'
        return representation
        

    