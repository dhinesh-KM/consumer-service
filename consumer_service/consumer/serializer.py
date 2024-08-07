from typing import Any, Dict
from rest_framework import serializers
from .models import Consumer
from common_utils.custom_exceptions import *
from .utils import *
from django.contrib import auth
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .dboperations import *
from django.contrib.auth import hashers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    country = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        mobile = attrs.get("mobile")

        if attrs["password"] != attrs["confirm_password"]:
            raise Validation_Error("Password does not match.")

        if not email and not mobile:
            raise Validation_Error("Either email or mobile must be provided.")

        if email and mobile:
            raise Validation_Error("Only one of email or mobile should be provided.")
        if email:
            if Consumer.objects(email=email).first():
                raise Custom_Error(
                    "This email is already in use. Please choose a different one.", status.HTTP_409_CONFLICT
                )

        if mobile:
            if Consumer.objects(mobile=mobile).first():
                raise Validation_Error(
                    "This mobile number is already in use. Please choose a different one."
                )
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):     
        con = consumer_find({"email": attrs.get("email")})
        if not hashers.check_password(attrs["password"], con.password):
            raise Validation_Error("Invalid credentials, please try again")
        return con    


class CitizenshipSerializer(serializers.Serializer):
    index = serializers.CharField(read_only=True)
    country = serializers.CharField()
    affiliation_type = serializers.CharField()
    work_address = serializers.CharField(required=False, allow_blank=True)
    home_address = serializers.CharField()
    mobile_phone = serializers.CharField(max_length=10)
    work_phone = serializers.CharField(required=False, allow_blank=True, max_length=10)
    alt_phone = serializers.CharField(required=False, allow_blank=True, max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get request from context
        print(self.context)
        request = self.context.get('request')
        try:
            if request:
                if request.method.upper() == 'PATCH':
                    for field in self.fields:
                        self.fields[field].required = False
        except:
            print("No request found in context")
            
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for field in self.fields:
            if representation[field] is None: representation[field]=''
        return representation
    
    def validate(self, attrs):
        affiliation = attrs.get("affiliation_type")
        if affiliation and affiliation not in ["citz", "dcitz", "pr", "tvs", "tvw"]:
            raise Validation_Error(
                "Affiliation_type must be one of the following values ['citz', 'dcitz', 'pr', 'tvs', 'tvw']"
            )
        return attrs
