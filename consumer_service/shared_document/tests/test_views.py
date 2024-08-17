from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from common_utils.test_setup import Test
from relationship.tests.test_views import SpecRelViewTest
from django.urls import reverse
from bson import ObjectId
from ..models import SharedDocument
import datetime
from unittest.mock import patch,MagicMock


client = APIClient()
class SharedDocViewTest(Test):
    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        self.docid1 = str(ObjectId())
        self.docid2 = str(ObjectId())
        self.docid3 = str(ObjectId())
        
        self.miss1 = {'data' : {'docname': ['voterid'], 'missingIds': [self.docid1]}}
        
        self.test_data = {
            "data": [ 
                        { "doctype": "personal", "docid": self.docid1},
                        { "doctype": "identity", "docid": self.docid2},
                        { "doctype": "identity", "docid": self.docid3}
         ]
        }
        
        data1 = {
            "relationship_id": str(self.spr1.id),
            "relationship_type": "consumer to consumer",
            "shared_with": self.con2['coffer_id'],
            "shared_by": self.con1['coffer_id'],
            "docid": self.docid1,
            "doctype": "identity",
        }
        
        self.shrdoc1 = SharedDocument(**data1)
        self.shrdoc1.save()
        
        data2 = {
            "relationship_id": str(self.spr1.id),
            "relationship_type": "consumer to consumer",
            "shared_with": self.con1['coffer_id'],
            "shared_by": self.con2['coffer_id'],
            "docid": self.docid2,
            "doctype": "identity",
        }
        
        self.shrdoc2 = SharedDocument(**data2)
        self.shrdoc2.save()
        
        # patch
        self.missing_ids_patcher = patch('shared_document.middleware.requests.post')
        self.document_details_patcher = patch('shared_document.middleware.requests.post')
        self.document_action_patcher = patch('shared_document.middleware.requests.get')

        # Start the patches
        self.mock_missing_ids = self.missing_ids_patcher.start()
        self.mock_document_details = self.document_details_patcher.start()
        self.mock_document_action = self.document_action_patcher.start()
        
        self.mock_response = MagicMock()
        
        self.sharedata = {'data': [
            {
                'docname': 'voterid', 
                'docid': 'ABC1111111', 
                'Id': '66c092a9536d1b453ad27056', 
                'doctype': 'voterid', 
                'category': 'citizen_primary', 
                'url': 'url', 
                'content_type': 'content_type'
                }, 
            {   'docname': 'passport', 
                'docid': 'ABC1111111', 
                'Id': '66c092ab536d1b453ad27057', 
                'doctype': 'passport', 
                'category': 'citizen_primary', 
                'url': 'url', 
                'content_type': 'content_type'
                }
            ]
        }
        
    def tearDown(self) -> None:
        self.missing_ids_patcher.stop()
        self.document_details_patcher.stop()
        self.document_action_patcher.stop()
        
        
        
    def test_share_docs_notacp(self):

        self.mock_response.json.return_value = {'data' : {'docname': ['voterid'], 'missingIds': [self.docid1]}}
        self.mock_missing_ids.return_value = self.mock_response        
        
        response = self.client.post(reverse("share_unshare_docs", kwargs ={'rel_id': self.spr1.id, 'action': 'share'}), self.test_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['msg'], 'Relationship not accepted.')
        
    def test_share_docs_doc404(self):
        self.spr1['isaccepted'] = True
        self.spr1.save()

        self.mock_response.json.return_value = {'data' : {'docname': ['voterid'], 'missingIds': [self.docid1]}}
        self.mock_missing_ids.return_value = self.mock_response      
          
        response = self.client.post(reverse("share_unshare_docs", kwargs ={'rel_id': self.spr1.id, 'action': 'share'}), self.test_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], f'Document with this ID {str(self.docid1)} not found')
        
    def test_share_docs_doc404s(self):
        self.spr1['isaccepted'] = True
        self.spr1.save()
        
        self.mock_response.json.return_value = {'data' : {'docname': ['voterid'], 'missingIds': [self.docid1, self.docid2]}}
        self.mock_missing_ids.return_value = self.mock_response
        
        response = self.client.post(reverse("share_unshare_docs", kwargs ={'rel_id': self.spr1.id, 'action': 'share'}), self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], f'Documents with these IDs {[str(self.docid1), str(self.docid2)]} not found')
        
    def test_share_docs(self):
        self.spr1['isaccepted'] = True
        self.spr1.save()
        s1 = SharedDocument.objects()
        print(len(s1))
        self.mock_response.json.return_value = {'data' : {'docname': ['voterid', 'pancard'], 'missingIds': []}}
        self.mock_missing_ids.return_value = self.mock_response
        
        response = self.client.post(reverse("share_unshare_docs", kwargs ={'rel_id': self.spr1.id, 'action': 'share'}), self.test_data, format='json')
        s2 = SharedDocument.objects()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], f'Documents shared with {self.con2.consumer_fullname()}.')
        self.assertNotEqual(len(s1),len(s2))
        
    def test_unshare_docs(self):
        self.spr1['isaccepted'] = True
        self.spr1.save()
        s1 = SharedDocument.objects()
        print(len(s1))
        self.mock_response.json.return_value = {'data' : {'docname': ['voterid', 'pancard'], 'missingIds': []}}
        self.mock_missing_ids.return_value = self.mock_response
        
        self.test_data = {
            "data": [ 
                        { "doctype": "personal", "docid": self.docid1},
                        { "doctype": "identity", "docid": self.docid1},
         ]
        }
        
        response = self.client.post(reverse("share_unshare_docs", kwargs ={'rel_id': self.spr1.id, 'action': 'unshare'}), self.test_data, format='json')
        print(response.data)

        s2 = SharedDocument.objects()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], f'Documents unshared with {self.con2.consumer_fullname()}.')
        self.assertEqual(len(s1),2)
        self.assertEqual(len(s2),1)
        
    def test_shared_by_me(self):

        self.mock_response.json.return_value = self.sharedata
        self.mock_document_details.return_value = self.mock_response
        
        response = self.client.get(reverse("by_me", kwargs ={'rel_id': self.spr1.id}),format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']),2)
        
    def test_shared_with_me(self):

        self.mock_response.json.return_value = self.sharedata
        self.mock_document_details.return_value = self.mock_response
        
        response = self.client.get(reverse("with_me", kwargs ={'rel_id': self.spr1.id}),format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']),2)
        
    def test_shared_action_404(self):
        
        self.spr1['isaccepted'] = True
        self.spr1.save()
        
        self.mock_response.json.return_value = {'msg': 'Document with this id 66c0a7006d6237129211e3f1 not found', 'status_code':404}
        self.mock_document_action.return_value = self.mock_response
        
        response = self.client.get(reverse("action", kwargs ={'rel_id': self.spr1.id, 'docid': self.docid1, 'action': 'view'}),format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['url'], f'Document with this id {self.docid1} not found')
        
    def test_shared_action(self):
        
        self.spr1['isaccepted'] = True
        self.spr1.save()
        
        self.mock_response.json.return_value = {'url': 'url'}
        self.mock_document_action.return_value = self.mock_response
        
        response = self.client.get(reverse("action", kwargs ={'rel_id': self.spr1.id, 'docid': self.docid1, 'action': 'view'}),format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], 'url')
        
        
        
    