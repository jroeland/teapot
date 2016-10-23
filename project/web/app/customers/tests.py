from django.test import TestCase, Client
from customers.models import Customer
from RestApi.testbase import BaseApiTestCase

#Test for the customer API
#See BaseApiTestCase for more details
class CustomerAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        d1 = {"name":"Coca Cola", "since":"2014-06-28", "revenue":"492.12", "uid" : "1"}
        Customer.objects.create(**d1)
        
    def test_get_all(self):
        queryset = Customer.objects.all()
        super(CustomerAPITestCase, self).test_get_all("/api/customers/", queryset)
        
    def test_get_one(self):
        queryset = Customer.objects.filter(uid = 1)
        super(CustomerAPITestCase, self).test_get_one("/api/customers/1/", queryset)
    
    def test_post(self):
        queryset = Customer.objects.filter(uid = 2)
        post_data = '{"name":"Teamleader", "since":"2015-01-15", "revenue":"1505.95", "uid" : "2"}'
        super(CustomerAPITestCase, self).test_post("/api/customers/", queryset, post_data)
        
        
    def test_put(self):
        queryset = Customer.objects.filter(uid = 1)
        put_data = '{"name":"Coca Cola", "since":"2014-06-28", "revenue":"1.00", "uid" : "1"}'
        super(CustomerAPITestCase, self).test_put("/api/customers/1/", queryset, put_data)
        self.assertEqual(queryset[0].revenue, 1)
        
        
    def test_delete(self):
        queryset = Customer.objects.filter(uid = 1)
        super(CustomerAPITestCase, self).test_delete("/api/customers/1/", queryset)
