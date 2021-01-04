from django.conf.urls import url
from django.urls import path
from .views import PersonView

urlpatterns = [
    # url(r'^upload/$', FileView.as_view(), name='file-upload'),
    path('person/view/', PersonView.as_view(), name='PersonView'),
]