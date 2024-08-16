from .views import *
from django.urls import path

urlpatterns = [
    path('<str:rel_id>/docs/<str:action>', SharedDocumentView.as_view(), name='share_unshare_docs'),
    path('<str:rel_id>/docs/shared/byme', SharedDocumentView.as_view(), name='by_me'),
    path('<str:rel_id>/docs/shared/withme', SharedDocumentView.as_view(), name='with_me'),
    path('<str:rel_id>/<str:docid>/<str:action>', SharedDocumentView.as_view(), name='action'),
] 