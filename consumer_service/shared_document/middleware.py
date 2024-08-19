from .models import SharedDocument
from rest_framework import status
from common_utils.custom_exceptions import CustomError
from common_utils.utils import spe_rel_by_id
from django.conf import settings
import requests,jwt



def missing_ids(request, relid):

    spe_rel_by_id(relid)
    
    token = request.headers.get("Authorization")
    doc = {'identity': [], 'personal': []}
    
    for item in request.data['data']:
        doc[item['doctype']].append(item['docid'])
        
    
    url = f'{settings.DOCUMENT_SERVICE}api/v1/document/idocs'
    headers = {'Authorization': token}
    
    identity_payload = {'docid' : doc['identity']}
    personal_payload = {'docid' : doc['personal']}

    result_data = requests.post(url, data = identity_payload, headers=headers)

    return  result_data.json()['data']
        


def document_details(request, relid):

    cofferid = request.con['coffer_id']
    url_name = request.resolver_match.url_name
    doc = {'identity': [], 'personal': []}
    token = request.headers.get("Authorization")
    result_data = []
    
    spr = spe_rel_by_id(relid).first()
    
    if url_name == 'by_me':
        if cofferid == spr['requestor_uid']: sharedBy = spr['requestor_uid']
        elif cofferid == spr['acceptor_uid']:  sharedBy = spr['acceptor_uid']
        
    if url_name == 'with_me':
        if cofferid == spr['requestor_uid']:  sharedBy = spr['acceptor_uid']
        elif cofferid == spr['acceptor_uid']:  sharedBy = spr['requestor_uid']
        
    documents = SharedDocument.objects(__raw__ = { 'relationship_id': relid, 'shared_by': sharedBy})
    
    for item in documents:
        doc[item['doctype']].append(item['docid'])
        
    personal_payload = { 'docid': doc['personal'] }
    identity_payload = { 'docid': doc['identity'] }
        

    url = f'{settings.DOCUMENT_SERVICE}api/v1/document/idocs/details'
    headers = {'Authorization': token}
    
    if len(doc['identity']) != 0:

        data = identity_payload
        idocs = requests.post(url, data, headers=headers)
        result_data.extend(idocs.json()['data'])
        
    
    '''if len(doc['identity']) != 0:
        
        data = personal_payload
        pdocs = requests.post(url, data, headers=headers)
        result_data.extend(pdocs.json()['data'])'''
 
    return {'data': result_data}
        
      
            
def document_action(request, **kwargs):

    token = request.headers.get("Authorization")
    headers = {'Authorization': token}
    url = f'{settings.DOCUMENT_SERVICE}api/v1/document/idocs/{kwargs['action']}/{kwargs['docid']}'
        
    relid = kwargs['rel_id']
    spr = spe_rel_by_id(relid).first()

    if not spr['isaccepted']:
        raise CustomError('Relationship not accepted.', status.HTTP_202_ACCEPTED)

    
    resp = requests.get(url, headers=headers)

    if resp.status_code == 404:
        raise CustomError(f'{resp.json()['msg']}', status.HTTP_404_NOT_FOUND)
        
    return resp.json()
        
       

    