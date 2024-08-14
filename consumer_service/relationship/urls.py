from .views import *
from django.urls import path

urlpatterns = [
    path('search', SpecRelView.as_view(), name='get_cons'),
    path('request', SpecRelView.as_view(), name='request_con'),
    path('<str:rel_id>/accept', SpecRelView.as_view(), name='accept_con'),
    path('', SpecRelView.as_view(), name='all_rel')
]