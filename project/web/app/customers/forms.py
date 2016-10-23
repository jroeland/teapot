'''
Created on Oct 18, 2016

@author: jaime
'''
from django import forms
from customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()