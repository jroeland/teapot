'''
Created on Oct 22, 2016

@author: jaime
'''
from django.core import serializers


class BaseApiTestCase(object):
    """
        Base test for the views using the TeapotApi
        To use, simply inherit from it in your tests and extend the method.
        When calling super, make sure to add the required parameters.
        
        Example of use:
        def test_post(self):
            queryset = Model.objects.filter(uid = 2)
            post_data = '{...}'
            response = super(CustomerAPITestCase, self).test_post("/api/customers/", queryset, post_data)
            ... Extra tests using response ...
        
        
        Tests that will be perfomed:
        - status codes
        - content types
        - content serialization
    """
    json_content_type = "application/json"
    def test_get_all(self,url, queryset):
        """
            To test that all the entries of a model are returned
            @param queryset: -> queryset: The queryset to compare data returned
            @param url: -> str: The url for the api to get all entries
            Returns the connection's response so further tests can be done 
        """
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], self.json_content_type)
        self.assertEqual(response.content, serializers.serialize("json", queryset))
        return response
        
    def test_get_one(self, url, queryset):
        """
            To test that one single entry  of a model is returned
            @param queryset: -> queryset: The queryset to compare data returned
            @param url: -> str: The url for the api to get one entry
            Returns the connection's response so further tests can be done 
        """
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], self.json_content_type)
        self.assertEqual(response.content, serializers.serialize("json", queryset))
        return response
     
    def test_post(self, url, queryset, post_data):
        """
            To test a post and that the new entry is returned
            @param queryset: -> queryset: The queryset to compare data changed
            @param url: -> str: The url for the api to post data
            @param post_data: -> str: Json serializable string containig the new values for a new entry
            Returns the connection's response so further tests can be done 
        """
        response = self.client.post(url, post_data, content_type = self.json_content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], self.json_content_type)
        self.assertEqual(response.content, serializers.serialize("json", queryset))
        return response
        
     
    def test_put(self, url, queryset, put_data):
        """
            To test that a put has saved the data and the entry updated is returned
            @param queryset: -> queryset: The queryset to compare data changed
            @param url: -> str: The url for the api to put data
            @param put_data: -> str: Json serializable string containig the new values for an entry
            Returns the connection's response so further tests can be done 
        """
        response = self.client.put(url, put_data, content_type = self.json_content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], self.json_content_type)
        self.assertEqual(response.content, serializers.serialize("json", queryset))
        return response
     
    def test_delete(self, url, queryset):
        """
            To test that an entry is effectively deleted
            @param queryset: -> queryset: The queryset of the item(s) to delete
            @param url: -> str: The url for the api to delete data
            Returns the connection's response so further tests can be done
        """
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(queryset.count(), 0)
        return response
