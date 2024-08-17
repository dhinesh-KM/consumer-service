from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from django.contrib.auth import hashers
import mongoengine,datetime
from consumer.models import Consumer
from relationship.models import SpecialRelationship
from shared_document.models import SharedDocument

client = APIClient()
class Test(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()
        # Connect to the test database
        mongoengine.disconnect(alias='default')
        cls.db = mongoengine.connect(db='test_my_database', host='mongodb://localhost')
        
        # Create test data
        cls.con1 = Consumer(
            email="vijay1@gmail.com",
            password=hashers.make_password("dev1"),
            country="india",
            first_name="dhinesh",
            last_name="kumar",
            coffer_id="0000",
            citizen = [{
                    "index": "citizen_primary",
                    "country": "Austria",
                    "affiliation_type": "citz",
                    "home_address": "brazil home address",
                    "mobile_phone": "9488840673"
                },
                {
                    "index": "citizen_second",
                    "country": "India",
                    "affiliation_type": "tvs",
                    "home_address": "brazil home address",
                    "mobile_phone": "9488840673"
                }]
        )
        cls.con1.save()
        cls.con2 = Consumer(
            email="vijay12@gmail.com",
            password=hashers.make_password("dev12"),
            country="india",
            first_name="dhinesh",
            last_name="kumar",
            coffer_id="1111"
        )
        cls.con2.save()
        
        cls.con3 = Consumer(
            email="vijay123@gmail.com",
            password=hashers.make_password("dev123"),
            country="india",
            first_name="dhinesh",
            last_name="kumar",
            coffer_id="2222"
        )
        cls.con3.save()
        
        cls.valid_data1 = {
            "email": "vijay12@gmail.com",
            "password": "dev12",
            "action":"login",
            "logintype":"email"
        }
        
        cls.valid_data2 = {
            "email": "vijay1@gmail.com",
            "password": "dev1",
            "action":"login",
            "logintype":"email"
        }
        
        cls.valid_data3 = {
            "email": "vijay123@gmail.com",
            "password": "dev123",
            "action":"login",
            "logintype":"email"
        }

        
        response1 = client.post(reverse("login"), cls.valid_data1, format="json")
        response2 = client.post(reverse("login"), cls.valid_data2, format="json")
        response3 = client.post(reverse("login"), cls.valid_data3, format="json")
        cls.token1 = response1.data['token']
        cls.token2 = response2.data['token']
        cls.token3 = response3.data['token']
        cls.id1 = cls.con1.id 
        cls.id2 = cls.con2.id 
        cls.id3 = cls.con3.id
        
        data1 = {
            'requestor_type' : 'consumer',
            'requestor_uid' : cls.con1['coffer_id'],
            'requestor_tags' : ['Personal'],
            'acceptor_type' : 'consumer',
            'acceptor_uid' : cls.con2['coffer_id'],
            'acceptor_tags' : ['Personal'],
            'created' : datetime.datetime.now(),
            'status' : 'requested',
            'description' : "accept the request",
        }
        
        data2 = {
            'requestor_type' : 'consumer',
            'requestor_uid' : cls.con3['coffer_id'],
            'requestor_tags' : ['Personal'],
            'acceptor_type' : 'consumer',
            'acceptor_uid' : cls.con1['coffer_id'],
            'acceptor_tags' : ['Personal'],
            'created' : datetime.datetime.now(),
            'status' : 'accepted',
            'description' : "accept the request",
        }
        
        
        
        cls.spr1 = SpecialRelationship(**data1)
        cls.spr1.save()
        
        cls.spr2 = SpecialRelationship(**data2)
        cls.spr2.save()
        
        

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        # Drop the test database
        cls.db.drop_database('test_my_database')
        cls.db.close()