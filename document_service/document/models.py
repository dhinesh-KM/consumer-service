from mongoengine import *

class IdentityDocument(Document):
    consumer = StringField()
    category = StringField()  # citizen_primary
    doctype = StringField()  # aadhar
    docid = StringField()  # aadhar-number
    expiration_date = DateTimeField()  # Expiration Date
    content_type = StringField()  # File Content-Type
    filename = StringField()    # File Name
    filesize = IntField()  # Integer Value # File Size
    created = DateTimeField()
    updated = DateTimeField()
    metadata = DictField()
    verification_status = StringField()
    validity_status = StringField()
    verification_vendor = StringField()
    ciphertext = StringField()
    tags = ListField(default=[])