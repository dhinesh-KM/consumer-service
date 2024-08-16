from .models import SharedDocument
from rest_framework import status
from common_utils.custom_exceptions import CustomError
from common_utils.utils import spe_rel_by_id
from django.conf import settings
import requests,jwt



def missings_ids(request):
        
    token = request.headers.get("Authorization")
    doc = {'identity': [], 'personal': []}
    
    for item in request.data['add']:
        doc[item['doctype']].append(item['docid'])
        
    
    url = f'{settings.DOCUMENT_SERVICE}/api/v1/document/idocs'
    headers = {'Authorization': token}
    
    identity_payload = {'docid' : doc['identity']}
    personal_payload = {'docid' : doc['personal']}
    
    result_data = requests.post(url, data = identity_payload, headers=headers)
    return  result_data.json()['data']
        


def document_details(request, kwargs):

    cofferid = request.con['coffer_id']
    url_name = request.resolver_match.url_name
    relid = kwargs['rel_id']
    doc = {'identity': [], 'personal': []}
    token = request.headers.get("Authorization")
    result_data = []
    
    spr = spe_rel_by_id(relid)
    
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
    
    url = f'{settings.DOCUMENT_SERVICE}/api/v1/document/idocs/details'
    headers = {'Authorization': token}
    
    if len(doc['personal']) != 0:
        
        data = identity_payload
        idocs = requests.post(url, data, headers=headers)
        data = idocs.json()['data']
        
    
    '''if len(doc['identity']) != 0:
        
        data = personal_payload
        pdocs = requests.post(url, data, headers=headers)
        data = pdocs.json()['data']'''
        
    return {'data':data}
        
      
            
def document_action(request, **kwargs):

    token = request.headers.get("Authorization")
    headers = {'Authorization': token}
    url = f'{settings.DOCUMENT_SERVICE}/api/v1/consumer/p-docs/{kwargs['action']}/{kwargs['docid']}'
    
    relid = kwargs['rel_id']
    spr = spe_rel_by_id(relid)

    if not spr.isaccepted:
        raise CustomError('Relationship not accepted.', status.ACCEPTED)

    resp = requests.get(url, headers=headers)

    return resp['data']
        
       

    