from rest_framework import serializers
from bson import ObjectId



class SharedDocSerializer(serializers.Serializer):
    doctype = serializers.CharField()
    docid = serializers.CharField()
    
    def validate(self, attrs):
        if not ObjectId.is_valid(attrs['docid']):
            raise serializers.ValidationError("Invalid ObjectId format.")
        return attrs
        
class SharedDocSerializer(serializers.Serializer):
    data = serializers.ListField( child = SharedDocSerializer)