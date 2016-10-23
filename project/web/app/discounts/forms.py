'''
Created on Oct 19, 2016

@author: jaime
'''
from django import forms
from discounts.models import FreeProduct, CategoryDiscount, LoyaltyDiscount

class FreeProductForm(forms.ModelForm):
    class Meta:
        model = FreeProduct
        exclude = ()


class CategoryDiscountForm(forms.ModelForm):
    class Meta:
        model = CategoryDiscount
        exclude = ()
        
class LoyaltyDiscountForm(forms.ModelForm):
    class Meta:
        model = LoyaltyDiscount
        exclude = ()