'''
Created on Oct 19, 2016

@author: jaime
'''
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from products import views
urlpatterns = [
    url(r'^categories/$', csrf_exempt(views.ProductCategoryView.as_view())),
    url(r'^categories/(?P<uid>\w+)/$', csrf_exempt(views.ProductCategoryView.as_view())),
    
    url(r'^$', csrf_exempt(views.ProductView.as_view())),
    url(r'^(?P<uid>\w+)/$', csrf_exempt(views.ProductView.as_view())),
    
    
]