import mongoengine,jwt,datetime
from rest_framework import status
from ..models import IdentityDocument
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from unittest.mock import patch,MagicMock
from bson import ObjectId



client = APIClient()
class Test(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()
        # Connect to the test database
        mongoengine.disconnect(alias='default')
        cls.db = mongoengine.connect(db='test_my_database', host='mongodb://localhost')

        
    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        # Drop the test database
        cls.db.drop_database('test_my_database')
        cls.db.close()
        
class IdocViewTest(Test):
    
    def setUp(self) -> None:
        
        self.valid = {
            'doctype': 'passport',
            'docid': '123456',
            'file': SimpleUploadedFile('test_file.txt', b'file content'),
            'tags': ['tag1'],
            'expiration_date': '14-08-2024'
        }
        
        
        
        self.req_data = {'data': {'coffer_id': 'ABCD11111','citizen': [{'index': 'citizen_primary', 'country': 'India'},
                                                                       {'index': 'citizen_second', 'country': 'China'}]}}
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer token')
        
        # Patch jwt.decode and requests.get once for all tests
        self.jwt_decode_patcher = patch('common_utils.authentication.jwt.decode')
        self.requests_get_patcher = patch('common_utils.authentication.requests.get')

        # Start the patches
        self.mock_jwt_decode = self.jwt_decode_patcher.start()
        self.mock_requests_get = self.requests_get_patcher.start()

        # Set up the return values for the mocks
        self.mock_jwt_decode.return_value = {'coffer_id': '1111111'}
        
        mock_response = MagicMock()
        mock_response.json.return_value = self.req_data
        self.mock_requests_get.return_value = mock_response
        
        data1 = {'doctype': 'voterid',
                'docid': 'ABC1111111',
                'tags': ['identity'],
                'verification_status' : 'NotVerified',
                'validity_status' : 'Valid',
                'category' : 'citizen_primary',
                'consumer' : 'ABCD11111',
                'filename' : 'filename',
                'filesize' : 2000,
                'content_type' : 'content_type',
                'created' : datetime.datetime.now()
            }
        data2 = {'doctype': 'passport',
                'docid': 'ABC1111111',
                'tags': ['identity'],
                'expiration_date': datetime.datetime.now(),
                'verification_status' : 'NotVerified',
                'validity_status' : 'Valid',
                'category' : 'citizen_primary',
                'consumer' : 'ABCD11111',
                'filename' : 'filename',
                'filesize' : 1000,
                'content_type' : 'content_type',
                'created' : datetime.datetime.now()
            }
        
        self.idoc1 = IdentityDocument(**data1)
        self.idoc1.save()
        self.idoc1.save_file(SimpleUploadedFile('test_file.txt', b'file content'))
        
        self.idoc2 = IdentityDocument(**data2)
        self.idoc2.save()
        self.idoc2.save_file(SimpleUploadedFile('test_file.txt', b'file content'))

        self.delete = True

    def tearDown(self) -> None:
        IdentityDocument.objects.all().delete()
        # Stop the patches
        self.jwt_decode_patcher.stop()
        self.requests_get_patcher.stop() 
        
        self.idoc1.delete_file()
        if self.delete:  
            self.idoc2.delete_file()
        
    def test_idoc_create_citz_notfound(self):
        response = self.client.post(reverse("CR_idoc", kwargs={'cat': 'citizen_third'}), self.valid, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'msg': 'Citizenship not found'}) 

    def test_idoc_create(self):
        
        response = self.client.post(reverse("CR_idoc", kwargs={'cat': 'citizen_primary'}), self.valid, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'msg': 'Document uploaded successfully!'}) 

    def test_idoc_create_noexp(self):
        
        del self.valid['expiration_date'] 

        response = self.client.post(reverse("CR_idoc", kwargs={'cat': 'citizen_primary'}), self.valid, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Expiration date is required', response.data['msg'])
        
    def test_idoc_create_invalid_doctype(self):
        
        self.valid['doctype'] = 'tfn' 

        response = self.client.post(reverse("CR_idoc", kwargs={'cat': 'citizen_primary'}), self.valid, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Doctype must be one of the following values ', response.data['msg'])
        
        
    def test_idoc_create_invalid_docid(self):
        
        self.valid['doctype'] = 'aadhar' 
        self.valid['docid'] = '1245' 

        response = self.client.post(reverse("CR_idoc", kwargs={'cat': 'citizen_primary'}), self.valid, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], 'Invalid aadhar ID format')
        
    def test_idoc_update(self):
        data = { 'docid': 'ABS1234567'}
        filter={'consumer': 'ABCD11111','category' : 'citizen_primary', 'doctype': 'voterid' }

        i1 = IdentityDocument.objects(**filter).first()
        response = self.client.patch(reverse("RUD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'voterid'}), data, format='json')
        i2 = IdentityDocument.objects(**filter).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Document updated successfully.')
        self.assertNotEqual(i1['docid'], i2['docid'])
        
    def test_idoc_update_pastdate(self):
        data = { 'expiration_date': '8-8-2024'}

        response = self.client.patch(reverse("RUD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passport'}), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], 'Expiration date should be a future date')
        
    def test_get_single_idoc(self):
        response = self.client.get(reverse("RUD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passport'}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        
    def test_get_single_idoc_notfound(self):
        response = self.client.get(reverse("RUD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passpor'}), format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], 'Document not found.')
        
    def test_get_all_idoc(self):
        
        response = self.client.get(reverse("CR_idoc", kwargs={'cat': 'citizen_primary'}) )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2) 
        
    def test_delete_idoc(self):
        self.delete = False
        filter = {'consumer': 'ABCD11111','category' : 'citizen_primary'}
        
        i1 = IdentityDocument.objects(**filter)
        print(len(i1))
        response = self.client.delete(reverse("RUD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passport'}) )
        i2 = IdentityDocument.objects(**filter)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Document deleted successfully.')
        self.assertNotEqual(len(i1), len(i2))
        
    def test_idoc_view(self):
        response = self.client.get(reverse("VD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passport', 'action': 'view'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url',response.data['data'] )
        
    def test_idoc_download(self):
        response = self.client.get(reverse("VD_idoc", kwargs={'cat': 'citizen_primary', 'doctype': 'passport', 'action': 'download'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url',response.data['data'] )
        
        
    def test_idoc_miss(self):
        
        response = self.client.post(reverse("missing_ids"), {'docid': [str(self.idoc1.id), str(self.idoc2.id), str(ObjectId())]}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_idoc_details(self):
        
        response = self.client.post(reverse("doc_details"), {'docid': [str(self.idoc1.id), str(self.idoc2.id), str(ObjectId())]}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        
    def test_idoc_action(self):
        
        response = self.client.get(reverse("action", kwargs={'action':'views', 'id':str(ObjectId())}), format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
    
        