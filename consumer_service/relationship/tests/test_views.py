from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from common_utils.test_setup import Test
from django.urls import reverse
from bson import ObjectId
from ..models import SpecialRelationship
import datetime


client = APIClient()
class SpecRelViewTest(Test):

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        
        self.data = {
            'description': "accept the request",
            'consumerId': str(self.id2)
        }
        
    
    def test_get_consumers(self):
        response = self.client.get(reverse("get_consumers"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(len(response.data['data'][0].keys()), 4)
        
    def test_relship_req_con_notfound(self):
        self.data['consumerId'] = str(ObjectId())
        response = self.client.post(reverse("request_con"), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_relship_req_con_ishim(self):
        self.data['consumerId'] = str(self.id1)
        response = self.client.post(reverse("request_con"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_relship_req_con_alreadyexist1(self):
        response = self.client.post(reverse("request_con"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['msg'], 'Relationship already exists')
        
    def test_relship_req_con_alreadyexist2(self):
        self.data['consumerId'] = str(self.id3)
        response = self.client.post(reverse("request_con"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['msg'], 'Relationship already exists')
        
    def test_relship_req(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        self.data['consumerId'] = str(self.id3)
        response = self.client.post(reverse("request_con"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], 'Request sent successfully.')
        
    def test_relship_acpt_already_acpt(self):
        
        self.spr1['status'] = 'accepted'
        self.spr1['isaccepted'] = True
        self.spr1.save()
        
        self.data = {'response': 'accept'}

        response = self.client.post(reverse("accept_con", kwargs={'rel_id': self.spr1.id}), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['msg'], 'Relationship already accepted.')
        
    def test_relship_acpt_not_permit(self):
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        self.data = {'response': 'accept'}

        response = self.client.post(reverse("accept_con", kwargs={'rel_id': self.spr2.id}), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['msg'], 'You are not permitted to accept the relationship')
        
    def test_relship_acpt(self):
        
        self.data = {'response': 'accept'}

        response = self.client.post(reverse("accept_con", kwargs={'rel_id': self.spr2.id}), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Relationship accepted successfully.')
        
    def test_get_relship(self):

        response = self.client.get(reverse("all_relationships"), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        
    '''def test_get_relship_bytag(self):
        self.spr2.requestor_tags = ['Lauditor']

        response = self.client.get(reverse("relationships_bytag", kwargs={'tag': 'Personal'}), format='json')
        print(response.data['data'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(len(response.data['data']), 2)
        
    def test_get_relship_tagcount(self):

        response = self.client.get(reverse("tag_count"), format='json')
        print(response.data['counts'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)'''
    
        
        
    