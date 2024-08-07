from settings import *
import mongoengine,sys

MONGODB_DATABASES = {
    "default": { "host": "mongodb+srv://dhineshkumarm:mongo%40123@cluster0.ibc28ov.mongodb.net/Consumer-DB" },
    "test": { "host": "mongodb://localhost:27017/test" }
}
print("***************")
def is_test():
    print("***************")
    print(sys.argv)
    if 'test' in sys.argv:
        return True
    else:
        return False
    
if is_test():
    db = "test"
else:
    db = "default"
    
mongoengine.connect(MONGODB_DATABASES[db]['host'])



