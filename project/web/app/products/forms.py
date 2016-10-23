'''
Created on Oct 19, 2016

@author: jaime
'''
from django import forms
from products.models import Product, ProductCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
        
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ()