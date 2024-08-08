from mongoengine import *
<<<<<<< HEAD
from .firebaseconfig import save_obj,signed_url,del_obj

class IdentityDocument(Document):
    consumer = StringField()
    category = StringField()  
    doctype = StringField()  
    docid = StringField()  
    expiration_date = DateTimeField() 
    content_type = StringField()  
    filename = StringField()    
    filesize = IntField()  
=======

class IdentityDocument(Document):
    consumer = StringField()
    category = StringField()  # citizen_primary
    doctype = StringField()  # aadhar
    docid = StringField()  # aadhar-number
    expiration_date = DateTimeField()  # Expiration Date
    content_type = StringField()  # File Content-Type
    filename = StringField()    # File Name
    filesize = IntField()  # Integer Value # File Size
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
    created = DateTimeField()
    updated = DateTimeField()
    metadata = DictField()
    verification_status = StringField()
    validity_status = StringField()
    verification_vendor = StringField()
    ciphertext = StringField()
<<<<<<< HEAD
    tags = ListField(default=[])
    
    def file_name(self):
        return f'con-{self.consumer}/pdoc-{str(self.id)}'
    
    def save_file(self):
        param = { 'contentType': self.content_type }
        return save_obj(self.file_name(),param)
    
    def view(self):
        #params = {'responseType' : self.content_type}
        return signed_url(self.file_name())
    
    def download(self):
        params = { 'response_disposition' : f'attachment; filename={self.filename}'} #responseType : this.content_type };
        return signed_url(self.file_name(),params)
    
    def delete_file(self):
        return del_obj(self.file_name())
     
=======
    tags = ListField(default=[])
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
