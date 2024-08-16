from .views import *
from django.urls import path

urlpatterns =[
    path('identity/<str:cat>', IdocView.as_view(), name='CR_idoc'),
    path('identity/<str:cat>/<str:doctype>', IdocView.as_view(), name='RUD_idoc'),
    path('identity/<str:cat>/<str:doctype>/<str:action>', IdocView.as_view(), name='VD_idoc'),
    path('idocs', IdocUtilView.as_view(), name='missing_ids'),
    path('idocs/details', IdocUtilView.as_view(), name='doc_details'),
    path('idocs/<str:action>/<str:id>', IdocUtilView.as_view(), name='action'),
]