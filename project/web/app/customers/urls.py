'''
Created on Oct 18, 2016

@author: jaime
'''
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from customers import views
urlpatterns = [
    url(r'^$', csrf_exempt(views.CustomerView.as_view())),
    url(r'^(?P<uid>\w+)/$', csrf_exempt(views.CustomerView.as_view())),
]
