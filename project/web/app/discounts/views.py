from discounts.models import CategoryDiscount, FreeProduct, LoyaltyDiscount
from discounts.forms import CategoryDiscountForm, FreeProductForm, LoyaltyDiscountForm
from RestApi.TeapotAPI import TeapotAPI
from django.views.generic import View
from django.http import HttpResponse
from utils.mixins import JSONResponseMixin
import json
from discounts.calculate_discounts import CalculateDiscounts
# Create your views here.

class CategoryDiscountView(TeapotAPI):
    def __init__(self, *args, **kwargs):
        super(CategoryDiscountView, self).__init__(*args, **kwargs)
        self.set_model(CategoryDiscount)
        self.set_modelform(CategoryDiscountForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("id")

class FreeProductView(TeapotAPI):
    def __init__(self, *args, **kwargs):
        super(FreeProductView, self).__init__(*args, **kwargs)
        self.set_model(FreeProduct)
        self.set_modelform(FreeProductForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("id")

class LoyaltyDiscountView(TeapotAPI):
    def __init__(self, *args, **kwargs):
        super(LoyaltyDiscountView, self).__init__(*args, **kwargs)
        self.set_model(LoyaltyDiscount)
        self.set_modelform(LoyaltyDiscountForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("id")


class CalculateDiscountsView(View, JSONResponseMixin):
    def post(self, request, uid = None):
        #Make sure we get the content as application/json
        content_type = request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE', ''))
        if content_type != "application/json":
            return HttpResponse("Post or put header must be 'application/json'", status = 400)
        
        #Load the sent json and convert to to a python representation
        payload = None
        try:
            payload = json.loads(request.body)
        except Exception as e:
            #Return 400 is the payload is not serializable (or not json)
            return HttpResponse("JSON is not serializable", status = 400)
        
        #now we have our data ready to check!
        cd = CalculateDiscounts(payload)
        processed_data = cd.set_discounts()
        
        return self.render_data_to_response(processed_data, status = 201)