'''
Created on Oct 18, 2016

@author: jaime
'''
from django.core import serializers
from django.http import HttpResponse
from decimal import Decimal
import json
class JSONBaseMixin(object):
    def get_json_response(self, content, **httpresponse_kwargs):
        """
            Construct an `HttpResponse` object with the content type set to json
        """
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

class JSONQuerysetResponseMixin(JSONBaseMixin):
    """
        Helper for class based views
        Useful when the response should be a json representation of a queryset
    """
    def render_queryset_to_response(self, context, **httpresponse_kwargs):
        """
            Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(serializers.serialize('json', context), **httpresponse_kwargs)

    
        
class JSONResponseMixin(JSONBaseMixin):
    """
        Helper for class based views
        Useful when the response should be a json representation of a python object
    """
    def render_data_to_response(self, context, **httpresponse_kwargs):
        """
            Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(self.convert_context_to_json(context), **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """
            Convert the context dictionary into a JSON object
            Note: Json does not support decimal serialization by default, so we use decimal_default to convert decimals to serializable floats
        """
        return json.dumps(context, default = self.decimal_default)
    
    def decimal_default(self, obj):
        """
            Unlike simplejson, json does not suport decimal serialization.
            So we check id the object given is a decimal and convert it to a float
        """
        if isinstance(obj, Decimal):
            return float(obj)
        return obj