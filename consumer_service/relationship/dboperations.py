from consumer.models import Consumer
from common_utils.custom_exceptions import CustomError
from common_utils.utils import spe_rel_by_id
from rest_framework import status
from .models import SpecialRelationship
import datetime
from itertools import chain


def get_consumer(coffer_id):
    return Consumer.objects(coffer_id__ne = coffer_id)


def request_consumer(data, con):

    acp = data['acceptor']

    if acp['coffer_id'] == con['coffer_id']:
        raise CustomError('Operation not permitted', status.HTTP_409_CONFLICT)
    
    filter = {'requestor_uid' : con['coffer_id'], 'acceptor_uid' : acp['coffer_id'] }
    spr = SpecialRelationship.objects(**filter).first()
    if spr:
        raise CustomError('Relationship already exists', status.HTTP_409_CONFLICT)
    else:
        filter = {'requestor_uid' : acp['coffer_id'], 'acceptor_uid' : con['coffer_id'] }
        spr =  SpecialRelationship.objects(**filter).first()
        if spr:
            raise CustomError('Relationship already exists', status.HTTP_409_CONFLICT)
        else:
            input_data = {
                        'requestor_type' : 'consumer',
                        'requestor_uid' : con['coffer_id'],
                        'requestor_tags' : ['Personal'],
                        'acceptor_type' : 'consumer',
                        'acceptor_uid' : acp['coffer_id'],
                        'acceptor_tags' : ['Personal'],
                        'created' : datetime.datetime.now(),
                        'status' : 'requested',
                        'description' : data['description'],
                    }
            SpecialRelationship(**input_data)
            
            print(f'\n----VitaGist Relationship request----\n\t\t ${con.consumer_fullname()} has requested you to confirm and accept the relationship with them')

            return { 'msg' : 'Request sent successfully.'}
        
def accept_consumer(data, con, relid):
    spr =  spe_rel_by_id(relid)
    print(spr.to_json())
    if spr.first()['isaccepted']:
        raise CustomError('Relationship already accepted.', status.HTTP_409_CONFLICT)
    
    if data['response'] == 'accept':
            if spr.first()['acceptor_uid'] != con['coffer_id']:
                raise CustomError('You are not permitted to accept the relationship', status.HTTP_409_CONFLICT)
            update_data = {'$set': {    'isaccepted' : True,
                                        'accepted_date' : datetime.datetime.now(),
                                        'status' : 'accepted'
            }}
            spr.update_one(**update_data)

    return { 'msg'  : 'Relationship accepted successfully.'}


def get_relationships(cofferid):
    spr1 = SpecialRelationship.objects.filter(requestor_uid = cofferid)
    spr2 = SpecialRelationship.objects.filter(acceptor_uid = cofferid)
    print(spr1, spr2)
    s = list(chain(spr1, spr2))
    print(s)
    return spr1
    