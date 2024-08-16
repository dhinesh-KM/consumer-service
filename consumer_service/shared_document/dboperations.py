from .models import SharedDocument
from common_utils.custom_exceptions import CustomError
from common_utils.utils import spe_rel_by_id, consumer_by_cofferid
from rest_framework import status


def share_docs(relid, docs, cofferid, data, action):
    sharedWith, err_Msg = "", name = "Documents", result_Msg
    spr  = spe_rel_by_id(relid)
    
    if not spr.isaccepted:
        raise CustomError("Relationship not accepted.", status.HTTP_202_ACCEPTED)
    
    for data in docs:
        id = docs[data].missingIds
        len = id.length
        if len != 0:
            if len == 1:
                err_Msg += f'{data} document with this ID {id} not found' 
            else:
                err_Msg += f'{data} documents with these IDs {id} not found'
             
    if err_Msg.length != 0: 
        raise CustomError(err_Msg, status.HTTP_404_NOT_FOUND)
    
    sharedWith = spr.acceptor_uid
    if sharedWith == cofferid:
        sharedWith = spr.requestor_uid
        
    con =  consumer_by_cofferid(sharedWith)
    if action == 'share':
        if len(data) == 1:
            name = docs[data[0].doctype].docname
        
        for item in data:
            shrdoc = SharedDocument.objects(__raw__ = { 'relationship_id': relid, 'docid': item['docid'] }).first()
            if shrdoc is None:
                rel_data = {
                            'relationship_id': relid,
                            'relationship_type': "consumer to consumer",
                            'shared_with': sharedWith,
                            'shared_by': cofferid,
                            'docid': item['docid'],
                            'doctype': item['doctype'],
                }
                shr = SharedDocument(**rel_data)
                shr.save()

        result_Msg = f'{name} shared with {con.consumer_fullname()}.'
        
    else:
        if len(data) == 1:
            name = docs[data[0]['doctype']]['docname']

        docids = []
        for item in data:
            docids.append(item['id'])

        SharedDocument.objects(__raw__ = { 'relationship_id': relid, 'docid': { '$in': docids }, 'shared_by': cofferid }).delete()
        
        result_Msg = f'{name} unshared with {con.consumer_fullname()}.'
        
    return { 'msg': result_Msg }


    
    
    
    
    

 




  
  