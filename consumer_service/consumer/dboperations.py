from .models import Consumer, Country
from .utils import consumer_find
from common_utils.custom_exceptions import Custom_Error
from django.contrib.auth import hashers
from rest_framework import status
from django.conf import settings
import jwt,os,datetime,json


INDIA_AFFILIATIONS = {
    "Permanent Resident": "pr",
    "Temporary Resident - Student": "tvs",
    "Temporary Resident - Work": "tvw",
    "OCI (Overseas Citizen of India)": "oci",
    "PIO (Person of Indian Origin)": "pio"
}

AFFILIATIONS = {
    "Permanent Resident": "pr",
    "Dual Citizenship": "dcitz",
    "Temporary Resident - Student": "tvs",
    "Temporary Resident - Work": "tvw"
}

def consumer_affiliations(country):
    affiliations = []

    if country == 'India':
        for name, type in INDIA_AFFILIATIONS.items():
            affiliations.append({
                "aflType": type,
                "aflName": name
            })

    else:
        for name, type in AFFILIATIONS.items():
            affiliations.append({
                "aflType": type,
                "aflName": name
            })

    return {"data": affiliations}

def generate_coffer_id():
    uid = os.urandom(8).hex().upper()
    if Consumer.objects(coffer_id=uid):
        generate_coffer_id()
    return uid


def consumer_create(data):
    country_data = {}
    country_data["index"] = "citizen_primary"
    country_data["country"] = data["country"]
    country_data["affiliation_type"] = "citz"
    country = Country(**country_data)
    data["email"] = data["email"].lower()
    data["coffer_id"] = generate_coffer_id()
    data["password"] = hashers.make_password(data["password"])
    data["joined"] = datetime.datetime.now()
    data["email_verified"] = False
    data["mobile_verified"] = False
    email_verification_token = os.urandom(8).hex()
    mobile_verification_token = os.urandom(3).hex().upper()
    con = Consumer(**data)
    con.citizen = [country]
    con.save()

    return {"msg": "Consumer created successfully."}


def consumer_login(con):

    payload = {
        "coffer_id": con.coffer_id,
        "pk": str(con.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    if con.lastlogin is None:
        print("==========>>>>>> SEND WELCOME EMAIL <<<<<<==========")
    con.lastlogin = datetime.datetime.now()
    con.save()
    return {'token' : token, 'con' : con }

def consumer_citizenship(data=None, action=None, con=None, citizen=None):

    citz_index = []
    for item in con.citizen:
        citz_index.append(item['index'])

    if citizen and citizen not in citz_index:
        raise Custom_Error('Citizenship not found.', status.HTTP_404_NOT_FOUND)
    
    if action == 'create':
        index = ''
        arr = ['citizen_primary','citizen_second','citizen_third','citizen_fourth']
        
        if len(citz_index) == 4:
            raise Custom_Error('Too many citizenships.', status.HTTP_409_CONFLICT)
        
        for item in citz_index:
            if item  in arr:
                arr.remove(item)
        index = arr[0]
        
        data['index'] = index
        country = Country(**data)   
        con.citizen.append(country)  
        con.save()
        return {'msg':'Citizenship created successfully.'}
    
    if action == 'update':
        
        for item in con.citizen:
            if item['index'] == citizen:
                for i in data:
                    item[i] = data[i]
        con.save()    
        return {'msg':'Citizenship updated successfully.'}
    
    if action == 'view':
        for item in con.citizen:
            if item['index'] == citizen:
                data = item.to_dict()
        return {'data': [data]}
    
    if action == 'delete':
        if citizen == 'citizen_primary':
            raise Custom_Error('Citizen primary cannot be deleted', status.HTTP_409_CONFLICT)
        con.citizen = [item for item in con.citizen if item['index'] != citizen]
        con.save()
        
        return {'msg': 'Citizenship deleted successfully.'}
                
                
                
        
