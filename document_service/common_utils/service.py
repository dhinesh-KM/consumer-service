from django.conf import settings

URL = f"{settings.CONSUMER_SERVICE}/api/v1/consumer"

Url = {
    'consumer_object' : { 'url': '{URL}/{coffer_id}'},
}

class API:
    def __getattr__(self,attr):
        def service_execution(urlparams=None, payload=None):
            pass
            