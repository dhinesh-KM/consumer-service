from .models import IdentityDocument
import datetime

def Idoc_operations(data=None, action=None, con=None, citz=None):
    
    if action == 'create':
        
        file = data['file']

        filter = {'consumer': con['coffer_id'], 'doctype': data['doctype'], 'category': citz['cat']}
        exist_idoc = IdentityDocument.objects(__raw__= filter)
        print(exist_idoc)
        if len(exist_idoc) == 1:
            update_data = {'$set': {
                        'docid': data['docid'],
                        'filename': file.name,
                        'filesize': file.size,
                        'content_type': file.content_type,
                        'created': datetime.datetime.now()
                        }}
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
            data['country'] = con['country']
            del data['file']
            del data['tags']
            
            idoc = IdentityDocument(**data)
            idoc.save()
            idoc.save_file(file)
        
        return {'msg': 'Document uploaded successfully!'}    
    
    if action == 'delete':
        filter = { 'consumer': con['coffer_id'], 'doctype': citz['doctype'], 'category': citz['cat']}
        idoc = IdentityDocument.objects(__raw__=filter)
        if len(idoc) == 1:
            idoc.first().del_obj()
            idoc.delete()
        return {'msg': 'Document deleted successfully.'}
            
        
        
        
        
        
        
    
    
    