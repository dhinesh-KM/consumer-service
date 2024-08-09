import firebase_admin,datetime,os
from firebase_admin import credentials,storage
import firebase_admin.storage


serviceaccount = os.path.join(os.path.dirname(__file__), 'serviceaccountkey.json')

firebase_admin.initialize_app(credentials.Certificate(serviceaccount), {
    'storageBucket' : 'fileuploads-82158.appspot.com'
})

bucket = storage.bucket() 

def signed_url(filename, params=None):
    
    file = bucket.blob(filename)

    #Configuration for url
    config = { 'method': 'GET', 'expiration' : datetime.timedelta(hours=1), 'version': 'v4' }
    if params:
        config.update(params)
    

    return file.generate_signed_url(**config)  

def save_obj(file, params):
    # Create a blob in Firebase Storage
    blob = bucket.blob(file)
    
    # Upload the file to Firebase Storage
    blob.upload_from_file(file_obj = params['file'], content_type=params['contentType'])
    
    return signed_url(file)


def del_obj(file):
    blob = bucket.blob(file)
    
    blob.delete()
    