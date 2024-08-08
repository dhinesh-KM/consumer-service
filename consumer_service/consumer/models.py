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
    
    def to_dict(self):
        return {
            'index': self.index,
            'country': self.country,
            'affiliation_type': self.affiliation_type,
            'work_address': self.work_address if self.work_address else '' ,
            'home_address': self.home_address if self.home_address else '',
            'mobile_phone': self.mobile_phone if self.mobile_phone else '',
            'work_phone': self.work_phone if self.work_phone else '',
            'alt_phone': self.alt_phone if self.alt_phone else ''
        }


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

    def consumer_Fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def custom_uid(self) -> str:
        custom_uid = None
        if self.email:
            custom_uid = self.email.replace(".", "").replace("@", "")
        if self.mobile:
            custom_uid = self.mobile
        return custom_uid

    def consumer_data(self) -> dict:
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "dob": self.dob.strftime("%d/%m/%Y") if self.dob != "" else "",
            "email": self.email,
            "mobile": self.mobile,
            "country": self.country,
            "citizen": list(
                map(
                    lambda citizen: {
                        "country": citizen.country,
                        "affiliation_type": citizen.affiliation_type,
                        "mobile_phone": citizen.mobile_phone or "",
                        "home_address": citizen.home_address or "",
                        "alt_phone": citizen.alt_phone or "",
                        "index": citizen.index,
                        "work_phone": citizen.work_phone or "",
                        "work_address": citizen.work_address or "",
                    },
                    self.citizen,
                )
            ),
            "joined": self.joined,
            "coffer_id": self.coffer_id,
            "email_verified": self.email_verified,
            "mobile_verified": self.mobile_verified,
        }


