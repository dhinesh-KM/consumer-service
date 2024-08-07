import mongoengine
from rest_framework import status
from ..models import Consumer,Country
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from django.contrib.auth import hashers

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
            coffer_id="0000"
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
        
        response1 = client.post(reverse("login"), cls.valid_data1, format="json")
        response2 = client.post(reverse("login"), cls.valid_data2, format="json")
        cls.token1 = response1.data['token']
        cls.token2 = response2.data['token']
        
        

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        # Drop the test database
        cls.db.drop_database('test_my_database')
        cls.db.close()

class LoginviewTest(Test):
    def setUp(self) -> None:
        self.valid_data = {
            "email": "vijay12@gmail.com",
            "password": "dev12",
            "action":"login",
            "logintype":"email"
        }

        self.invalid_data = {
            "email": "vijay1@gmail.com",
            "password": "dev12",
            "action":"login",
            "logintype":"email"
        }

    def test_login_valid(self):
        response = self.client.post(reverse("login"), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['coffer_id'], "1111")

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("login"), self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_unknown_user(self):
        self.valid_data['email'] ="arun@gmail.com"
        response = self.client.post(reverse("login"), self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], 'Consumer not found')
        
class CitizenshipviewTest(Test):
    def setUp(self):
        self.valid = {
            "country": "Austria",
            "affiliation_type": "tvs",
            "home_address": "brazil home address",
            "mobile_phone": "9488840673"
        }
        citz1 = {
            "country": "Austria",
            "affiliation_type": "citz",
            "home_address": "brazil home address",
            "mobile_phone": "9488840673"
            }
        citz2 ={
            "country": "India",
            "affiliation_type": "tvs",
            "home_address": "brazil home address",
            "mobile_phone": "9488840673"
            }
        self.cat = 'citizen_second'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        self.client.post(reverse("CR_citizenship"), citz1, format="json")
        self.client.post(reverse("CR_citizenship"), citz2, format="json")
        
                
    def test_create_valid_citz(self):
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        response = client.post(reverse("CR_citizenship"), self.valid, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_citz_authorize(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.post(reverse("CR_citizenship"), self.valid, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_citz_affiliation(self):
        self.valid['affiliation_type'] = 'tv'
        response = self.client.post(reverse("CR_citizenship"), self.valid, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_citz(self):
        response = self.client.get(reverse("CR_citizenship"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_citz_notfound(self):
        response = self.client.get(reverse("RUD_citzenship", kwargs={'cat': 'citizen'}), format="json" )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_single_citz(self):
        response = self.client.get(reverse("RUD_citzenship", kwargs={'cat': 'citizen_second'}), format="json" )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['index'], 'citizen_second')
