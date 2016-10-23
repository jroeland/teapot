'''
Created on Oct 19, 2016

@author: jaime

Came up with the name while drinking a cup of tea :)
'''
from django.http import HttpResponse
from django.views.generic import View
from utils.mixins import JSONResponseMixin, JSONQuerysetResponseMixin
from django.shortcuts import get_object_or_404
import json

class TeapotAPI(JSONResponseMixin, JSONQuerysetResponseMixin, View):
    
    def __init__(self, *args, **kwargs):
        super(TeapotAPI, self).__init__(*args, **kwargs)
        #Init main attributes
        self.allowed_methods = []
        self.model = None
        self.modelform = None
        self.lookup_field = "id"
        
    def set_model(self, model):
        """
            Sets the model to use
            @param model: ModelClass reference
        """
        self.model = model
    
    def set_modelform(self, modelform):
        """
            Sets the modelform to use to validate the data sent for post and put
            @param: modelform: ModelForm / Form reference
        """
        self.modelform = modelform
    
    def set_allowed_methods(self, methods):
        """
            Set which methods are available for this end-point
            options are: post, put, get, delete
            @param methods: list of strings -> Example: ("post","put")
        """
        self.allowed_methods = methods
    
    def set_lookup_field(self, field):
        """
            Set which field in the model to use when querying the db
            Useful when the main key is not the default "id" field, but another one
            Its strongly recommended that the field passed should be unique
            @param field: string -> A field in the Model passed 
        """
        self.lookup_field = field
    
    def get(self, request, uid = None):
        if "get" not in self.allowed_methods:
            return HttpResponse("Method not allowed: get", status = 405)
        
        #If uid is not given in the parameter as url, return details of all instances
        data = self.model.objects.all()
        if uid:
            #If uid is given, just return details of this instance
            #The django serializer needs a list of data or it crashes
            data = [get_object_or_404(data, **{self.lookup_field : uid})]
        return self.render_queryset_to_response(data)
    
    def post(self, request, uid = None):
        if "post" not in self.allowed_methods:
            return HttpResponse("Method not allowed: post", status = 405)
        
        #The post method must not reference an existing instance
        if uid:
            return HttpResponse("Posts must not contain id parameter in url", status = 400)
        
        #Send the request to the post_or_put handler, since both of them behave similar
        return self._post_or_put(request)
    
    def put(self, request, uid = None):
        if "put" not in self.allowed_methods:
            return HttpResponse("Method not allowed: put", status = 405)
        
        #The put method must reference an existing instance
        if not uid:
            return HttpResponse("No id parameter sent in url", status = 400)
        
        #Send the request to the post_or_put handler, since both of them behave similar
        return self._post_or_put(request, uid = uid)
    
    def delete(self, request, uid = None):
        if "delete" not in self.allowed_methods:
            return HttpResponse("Method not allowed: delete", status = 405)
        #The delete method must reference an existing instance
        if not uid:
            return HttpResponse("No id parameter sent in url", status = 400)
        
        #Delete the object or return 404 if not found
        get_object_or_404(self.model, **{self.lookup_field : uid}).delete()
        return HttpResponse(status = 204)
    
    def _post_or_put(self, request, uid = None):
        
        #Make sure we get the content as application/json
        content_type = request.META.get('HTTP_CONTENT_TYPE', request.META.get('CONTENT_TYPE', ''))
        if content_type != "application/json":
            return HttpResponse("Post or put header must be 'application/json'", status = 400)
        
        payload = None
        instance = None
        
        #Load the sent json and convert to to a python representation
        try:
            payload = json.loads(request.body)
        except Exception as e:
            #Return 400 is the payload is not serializable (or not json)
            return HttpResponse("JSON is not serializable", status = 400)
        
        #A put request will contain the uid
        if uid:
            #Get the instance to change or if it doesn't exist, return 404
            instance = get_object_or_404(self.model, **{self.lookup_field : uid})
            
        #This form validates the data before saving it to the db
        valitation_form = self.modelform(payload, instance = instance)
        if valitation_form.is_valid():
            #Data is valid, we may save now!
            data = valitation_form.save()
            #Return a serialized version of the data created/updated
            return self.render_queryset_to_response([data], status = 201)
        #Form did not validate... something is wrong with the data sent!
        return HttpResponse("Data did not validate: %s" % valitation_form.errors, status = 400)