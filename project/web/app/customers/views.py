from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from utils.mixins import JSONResponseMixin, JSONQuerysetResponseMixin
from customers.models import Customer
from customers.forms import CustomerForm
from django.shortcuts import get_object_or_404
import json
from RestApi.TeapotAPI import TeapotAPI
from website.settings import LOG

class CustomerView(TeapotAPI):
    """/api/customers/ endpoint"""
    
    def __init__(self, *args, **kwargs):
        super(CustomerView, self).__init__(*args, **kwargs)
        self.set_model(Customer)
        self.set_modelform(CustomerForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("uid")
    