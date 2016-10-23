'''
Created on Oct 19, 2016

@author: jaime
'''
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from discounts import views
urlpatterns = [
    url(r'^categories/$', csrf_exempt(views.CategoryDiscountView.as_view())),
    url(r'^categories/(?P<uid>\w+)/$', csrf_exempt(views.CategoryDiscountView.as_view())),
    url(r'^freeproducts/$', csrf_exempt(views.FreeProductView.as_view())),
    url(r'^freeproducts/(?P<uid>\w+)/$', csrf_exempt(views.FreeProductView.as_view())),
    url(r'^loyalty/$', csrf_exempt(views.LoyaltyDiscountView.as_view())),
    url(r'^loyalty/(?P<uid>\w+)/$', csrf_exempt(views.LoyaltyDiscountView.as_view())),
    
    url(r'^calculate/$', csrf_exempt(views.CalculateDiscountsView.as_view())),
]