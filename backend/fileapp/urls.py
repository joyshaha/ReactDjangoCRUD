from django.conf.urls import url
from django.urls import path
from .views import FileView

urlpatterns = [
    # url(r'^upload/$', FileView.as_view(), name='file-upload'),
    path('file/upload/', FileView.as_view(), name='file-upload'),
]