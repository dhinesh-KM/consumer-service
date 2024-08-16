from rest_framework import serializers
from bson import ObjectId

class ObjectIdField(serializers.CharField):
    def to_internal_value(self, data):

        if not ObjectId.is_valid(data):
            raise serializers.ValidationError("Invalid ObjectId format.")
        return str(data)

    def to_representation(self, value):
        # Ensure that the output is always a string
        return str(value)

class SharedDocSerializer(serializers.Serializer):
    doctype = serializers.CharField()
    docid = serializers.CharField()