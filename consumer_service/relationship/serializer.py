from rest_framework import serializers, status
from consumer.models import Consumer
from common_utils.custom_exceptions import CustomError,Not_Found
from common_utils.utils import consumer_by_cofferid


class GetConSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    id = serializers.CharField(required=False)
    
class SpecRelReqSerializer(serializers.Serializer):
    description = serializers.CharField()
    consumerId = serializers.CharField()
    
    def validate(self, attrs):
        con = Consumer.objects(id=attrs['consumerId']).first()
        if con == None:
            raise Not_Found('Consumer not found')
        attrs['acceptor'] = con
        return attrs
    
class SpecRelAcpSerializer(serializers.Serializer):
    response = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['response'] not in ['accept']:
            raise CustomError('response value should be "accept"', status.HTTP_400_BAD_REQUEST)
        return attrs
    
class SpecRelSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, default=True)
    isSpecial = serializers.BooleanField(required=False)
    canAccept = serializers.BooleanField(required=False, default=False)
    business_name = serializers.CharField(required=False)
    business_category = serializers.CharField(required=False, default='')
    products = serializers.ListField(child = serializers.CharField(), required=False, default= [])
    description = serializers.CharField(required=False,  default='')
    isaccepted = serializers.BooleanField(required=False, default=False)
    isarchived = serializers.BooleanField(required=False, default=False)
    status = serializers.CharField(required=False) 
    documents = serializers.DictField(required=False, default={})
    profile = serializers.DictField(required=False, default={})
    biztype =  serializers.CharField(required=False) 
    email = serializers.CharField(required=False, default='') 
    mobile = serializers.CharField(required=False, default='') 
    guid = serializers.CharField(required=False) 
    tags = serializers.ListField(child = serializers.CharField(), required=False)
    profileUrl = serializers.CharField(required=False, default='') 
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        coffer_id = self.context.get('con')
        if instance['requestor_uid'] == coffer_id:
            con = consumer_by_cofferid(instance['acceptor_uid'])
            representation['biztype'] = 'consumer'
            representation['business_name'] = con.consumer_fullname()
            representation['guid'] = con.custom_uid()
            #representation['profileUrl'] =  ''
            representation['tags'] = ['Personal']

        if instance['acceptor_uid'] == coffer_id:
            con = consumer_by_cofferid(instance['requestor_uid'])
            representation['biztype'] = 'consumer'
            representation['business_name'] = con.consumer_fullname()
            representation['guid'] = con.custom_uid()
            #representation['profileUrl'] =  ''
            representation['tags'] = ['Personal']
            
            representation['can_accept'] = True if representation['isaccepted'] == False else False
            
        return representation
            
    
    '''id = serializers.SerializerMethodField()
    isSpecial = serializers.SerializerMethodField()
    canAccept = serializers.SerializerMethodField()
    business_name = serializers.SerializerMethodField()
    business_category = serializers.CharField(required=False, default='')
    products = serializers.ListField(child = serializers.CharField(), default= [])
    description = serializers.SerializerMethodField(required=False, default='')
    isaccepted = serializers.SerializerMethodField()
    isarchived = serializers.BooleanField(required=False, default=False)
    status = serializers.SerializerMethodField() 
    documents = serializers.DictField(required=False, default={})
    profile = serializers.DictField(required=False, default={})
    biztype =  serializers.SerializerMethodField() 
    email = serializers.SerializerMethodField() 
    mobile = serializers.SerializerMethodField() 
    guid = serializers.SerializerMethodField() 
    tags = serializers.SerializerMethodField() 
    profileUrl = serializers.CharField(required=False, default='')'''
    
    
    '''def get_id(self,obj):
        print("**********",obj)
        con = self.context.get('con')
        print(con)
        print(self.instance.to_json())
        return con'''
    
'''class ConsumerSerializer(serializers.Serializer):
    biztype =  serializers.CharField(required=False) 
    business_name = serializers.CharField(required=False)
    guid = serializers.CharField(required=False) 
    tags = serializers.CharField(child = serializers.CharField(), required=False)
    profileUrl = serializers.CharField(required=False) '''
    
    
    
    