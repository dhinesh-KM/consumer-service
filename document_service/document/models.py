from mongoengine import *
from .firebaseconfig import save_obj,signed_url,del_obj 

class IdentityDocument(Document):
    consumer = StringField()
    category = StringField() 
    doctype = StringField()  
    docid = StringField()  
    country = StringField()
    expiration_date = DateTimeField() 
    content_type = StringField()  
    filename = StringField()   
    filesize = IntField()  
    created = DateTimeField()
    updated = DateTimeField()
    metadata = DictField()
    verification_status = StringField()
    validity_status = StringField()
    verification_vendor = StringField()
    ciphertext = StringField()
    tags = ListField(default=['Identity'])
    
    meta = {'collection': 'Identity documents', "indexes": ["consumer"]}
    
    def file_name(self):
        return f'con-{self.consumer}/Idoc-{str(self.id)}'
    
    def save_file(self, file):
        param = { 'contentType': self.content_type, 'file': file }
        return save_obj(self.file_name(),param)
    
    
    def download(self):
        params = { 'response_disposition' : f'attachment; filename={self.filename}'} #responseType : this.content_type };
        return signed_url(self.file_name(),params)
    
    def delete_file(self):
        return del_obj(self.file_name())
    
    def url(self):
        return signed_url(self.file_name())
    

