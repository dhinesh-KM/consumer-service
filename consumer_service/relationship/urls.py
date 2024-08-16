from .views import *
from django.urls import path

urlpatterns = [
    path('search', SpecRelView.as_view(), name='get_consumers'),
    path('request', SpecRelView.as_view(), name='request_con'),
    path('<str:rel_id>/accept', SpecRelView.as_view(), name='accept_con'),
    path('', SpecRelView.as_view(), name='all_relationships'),
    path('bytag/<str:tag>', SpecRelView.as_view(), name='relationships_bytag'),
    path('tagcount', SpecRelView.as_view(), name='tag_count'),
]