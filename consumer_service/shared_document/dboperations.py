from .models import SharedDocument
from common_utils.custom_exceptions import CustomError
from common_utils.utils import spe_rel_by_id, consumer_by_cofferid
from rest_framework import status


def share_docs(relid, docs, cofferid, data, action):
    sharedWith = ''
    err_msg = ''
    name = "Documents"
    result_msg = ''

    spr  = spe_rel_by_id(relid).first()
    
    if not spr['isaccepted']:
        raise CustomError("Relationship not accepted.", status.HTTP_202_ACCEPTED)
    
    print("///",docs)
    id = docs['missingIds']
    length = len(id)
    print(id)
    if length != 0:
        if length == 1:
            err_msg += f'Document with this ID {id[0]} not found' 
        else:
            err_msg += f'Documents with these IDs {id} not found'
             
    if len(err_msg) != 0: 
        raise CustomError(err_msg, status.HTTP_404_NOT_FOUND)
    
    sharedWith = spr['acceptor_uid']
    if sharedWith == cofferid:
        sharedWith = spr['requestor_uid']
        
    con =  consumer_by_cofferid(sharedWith)
    if action == 'share':
        if len(data) == 1:
            name = docs['docname'][0]
        
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

        result_msg = f'{name} shared with {con.consumer_fullname()}.'
        
    else:
        if len(data) == 1:
            name = docs['docname'][0]

        docids = []
        for item in data:
            docids.append(item['docid'])

        print(docids,relid,cofferid)
        f = { 'relationship_id': relid, 'docid': { '$in': docids }, 'shared_by': cofferid }
        d = SharedDocument.objects(**f)
        print('==',d)
        s = SharedDocument.objects(__raw__ = { 'relationship_id': relid, 'docid': { '$in': docids }, 'shared_by': cofferid }).delete()
        print(s)
        result_msg = f'{name} unshared with {con.consumer_fullname()}.'
        
    return { 'msg': result_msg }


    
    
    
    
    

 




  
  