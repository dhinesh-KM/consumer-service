from mongoengine import *

class SharedDocument(Document):
    #b2brelationship = ReferenceField(B2BRelationship)
    #relationship = ReferenceField(Relationship)
    relationship_id = StringField()
    docref = GenericLazyReferenceField()
    relationship_type = StringField()
    shared_with = StringField()
    shared_by = StringField()
    docid = StringField()
    doctype = StringField()
    docversion = StringField()