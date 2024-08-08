import firebase_admin,datetime
from firebase_admin import credentials,storage
import firebase_admin.storage
from document import se

firebase_admin.initialize_app({
    'credential' : credentials.Certificate('serviceaccountkey.json'),
    'storageBucket' : 'gs://fileuploads-82158.appspot.com'
})

bucket = storage.bucket() 

def signed_url(filename, params=None):
    
    file = bucket.blob(filename)

    #Configuration for url
    config = { 'method': 'GET', 'expiration' : datetime.timedelta(hours=1), 'version': 'v4' }
    config.update(params)
    
    #return array of string
    [url] = file.generate_signed_url(config)  
    return url

def save_obj(file):
    
    # Create a blob in Firebase Storage
    blob = bucket.blob(file)
    
    # Upload the file to Firebase Storage
    blob.upload_from_file(file, content_type=file.content_type)
    
    return signed_url(file)

def del_obj(file):
    blob = bucket.blob(file)
    
    blob.delete()
    