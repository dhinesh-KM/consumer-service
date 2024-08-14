from mongoengine import *


class Country(EmbeddedDocument):
    index = StringField()
    country = StringField()
    affiliation_type = StringField()
    work_address = StringField()
    home_address = StringField()
    mobile_phone = StringField()
    work_phone = StringField()
    alt_phone = StringField()
    affiliation_countryid = StringField()
    


class Consumer(Document):
    coffer_id = StringField(unique=True)
    first_name = StringField()
    middle_name = StringField()
    last_name = StringField()
    country = StringField()
    gender = StringField()
    username = StringField()
    password = StringField()
    confirm_password = StringField()
    password_reset_token = StringField()
    password_reset_timestamp = DateField()
    password_mode = StringField()
    joined = DateTimeField()
    lastlogin = DateTimeField()
    dob = DateField()
    email = StringField()
    mobile = StringField()
    email_verified = BooleanField(default=False)
    mobile_verified = BooleanField(default=False)
    email_verification_token = StringField()
    mobile_verification_token = StringField()
    citizen = EmbeddedDocumentListField(Country)

    meta = {"indexes": ["coffer_id"]}

    def consumer_fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def custom_uid(self) -> str:
        custom_uid = None
        if self.email:
            custom_uid = self.email.replace(".", "").replace("@", "")
        if self.mobile:
            custom_uid = self.mobile
        return custom_uid

    