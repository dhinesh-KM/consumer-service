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
            spr = SpecialRelationship(**input_data)
            
            spr.save()
            
            print(f'\n----VitaGist Relationship request----\n\t\t ${con.consumer_fullname()} has requested you to confirm and accept the relationship with them')

            return { 'msg' : 'Request sent successfully.'}
        
def accept_consumer(data, con, relid):
    spr =  spe_rel_by_id(relid)

    if spr.first()['isaccepted']:
        raise CustomError('Relationship already accepted.', status.HTTP_409_CONFLICT)

    if data['response'] == 'accept':
        
            if spr.first()['acceptor_uid'] != con['coffer_id']:
                raise CustomError('You are not permitted to accept the relationship', status.HTTP_409_CONFLICT)
            
            update_data = {'$set': {    'isaccepted' : True,
                                        'accepted_date' : datetime.datetime.now(),
                                        'status' : 'accepted'
            }}

            spr.update_one(__raw__= update_data)

    return { 'msg'  : 'Relationship accepted successfully.'}

#get all relationship, by tag, tag count
def get_relationships(cofferid, tag=None, action=None):
        '''if tag is not None:
            spr1 = list(SpecialRelationship.objects(requestor_uid = cofferid, requestor_tags = tag))
            spr2 = list(SpecialRelationship.objects(acceptor_uid = cofferid, acceptor_tags = tag))
        else:'''
        
        spr1 = list(SpecialRelationship.objects(requestor_uid = cofferid))
        spr2 = list(SpecialRelationship.objects(acceptor_uid = cofferid))
        
        '''if action == 'count':
            spr = spr1 + spr2
            
            tag = { 'Personal': 0, 'ContentCoffer': 0, 'Lauditor': 0 }
            tag_count = []
            
            for item in spr:
                if item['requestor_uid'] == cofferid:
                    tag[item['requestor_tags'][0]] += 1
                    
                if item['acceptor_uid'] == cofferid:
                    tag[item['acceptor_tags'][0]] += 1
                    
            for key, value in tag.items():
                if value > 0:
                    tag_count.append({ 'tagName': key, 'count': value })
                    
            return tag_count'''
        
        return spr1 + spr2


    
    
        
            
    