from .models import IdentityDocument
import datetime
from common_utils.custom_exceptions import Custom_Error
from rest_framework import status
from common_utils.utils import doctype_validate

def idoc_by_filter( action=None, **filter):

    idoc = IdentityDocument.objects(**filter)

    if len(idoc) == 0:
        raise Custom_Error('Document not found.', status.HTTP_404_NOT_FOUND)
    
    return idoc if action == 'update' else idoc.first()


def idoc_operations(data=None, action=None, con=None, citz=None):

    if action == 'create':
        file = data['file']
        
        filter = {'consumer': con['coffer_id'], 'doctype': data['doctype'], 'category': citz['cat']}
        
        exist_idoc = IdentityDocument.objects(**filter)
        
        if len(exist_idoc) == 1:
            update_data = {'$set': {
                        'docid': data['docid'],
                        'filename': file.name,
                        'filesize': file.size,
                        'content_type': file.content_type,
                        'created': datetime.datetime.now()
                        }}
            if 'expiration_date' in data:
                update_data['$set'].update({'expiration_date': data['expiration_date']})
            
            exist_idoc.first().save_file(file)
            
            exist_idoc = exist_idoc.update_one(__raw__ = update_data )
            
        else: 
            data['category'] = citz['cat']
            data['consumer'] = con['coffer_id']
            data['filename'] = file.name
            data['filesize'] = file.size
            data['content_type'] = file.content_type
            data['created'] = datetime.datetime.now()
            data['verification_status'] = 'NotVerified'
            data['validity_status'] = 'Valid'
            data['country'] = citz['country']

            del data['file']
            del data['tags']
            
            idoc = IdentityDocument(**data)
            
            idoc.save()
            
            idoc.save_file(file)
            
        
        return {'msg': 'Document uploaded successfully!'}    
    
    if action == 'get_all':
        filter = { 'consumer': con['coffer_id'], 'category': citz['cat']}
        return IdentityDocument.objects(**filter)
    
    if action == 'update':
        
        if len(data) > 0: 
            filter = { 'consumer': con['coffer_id'], 'doctype': citz['doctype'], 'category': citz['cat']}
            idoc = idoc_by_filter(action='update', **filter)
            
            if 'docid' in data:
                doctype_validate(citz['country'], citz['doctype'], data['docid'])
                
            update_data = { '$set':data}

            idoc.update_one(__raw__ = update_data)
        return {'msg': 'Document updated successfully.'}
    
    if action in ['get_one', 'delete', 'view', 'download']:
        filter = { 'consumer': con['coffer_id'], 'category': citz['cat'], 'doctype': citz['doctype']}
        idoc =  idoc_by_filter(**filter)
        
        if action == 'get_one':
            return idoc
            
        if action == 'delete':
            idoc.delete_file()
            idoc.delete()
            return {'msg': 'Document deleted successfully.'}
        
        if action == 'view':
            return {'url': idoc.url()}
        
        if action == 'download':
            return {'url': idoc.download()}
        
        

        
        
        
        
        
            
        
        
        
        
        
        
    
    
    