from django.test import TestCase, Client
from products.models import Product, ProductCategory
from discounts.models import CategoryDiscount, FreeProduct, LoyaltyDiscount
from RestApi.testbase import BaseApiTestCase
import json

#Test for the free product API
#See BaseApiTestCase for more details
class FreeProductAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        c1 = {"description":"Tools", "id" : "1"}
        self.productcategory = ProductCategory.objects.create(**c1)
        p1 = {"uid":"A101", "description":"Screwdriver", "category":self.productcategory, "price":"9.75"}
        self.product = Product.objects.create(**p1)
        fp = {"product":self.product, "quantity_required":5}
        self.freeproduct = FreeProduct.objects.create(**fp)
        
    def test_get_all(self):
        queryset = FreeProduct.objects.all()
        super(FreeProductAPITestCase, self).test_get_all("/api/discounts/freeproducts/", queryset)
        
    def test_get_one(self):
        queryset = FreeProduct.objects.filter(id = self.freeproduct.id)
        super(FreeProductAPITestCase, self).test_get_one("/api/discounts/freeproducts/1/", queryset)
    
    def test_post(self):
        queryset = FreeProduct.objects.filter(id = 2)
        post_data = '{"product":"%s", "quantity_required":"9"}' % self.product.uid
        super(FreeProductAPITestCase, self).test_post("/api/discounts/freeproducts/", queryset, post_data)
        
    def test_put(self):
        queryset = FreeProduct.objects.filter(id = self.freeproduct.id)
        put_data = '{"product":"%s", "quantity_required":"10"}' % self.product.uid
        super(FreeProductAPITestCase, self).test_put("/api/discounts/freeproducts/1/", queryset, put_data)
        self.assertEqual(queryset[0].quantity_required, 10)
        
    def test_delete(self):
        queryset = FreeProduct.objects.filter(id = self.freeproduct.id)
        super(FreeProductAPITestCase, self).test_delete("/api/discounts/freeproducts/1/", queryset)

#Test for the category discount API
#See BaseApiTestCase for more details
class CategoryDiscountAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        c1 = {"description":"Tools", "uid" : "1"}
        self.productcategory = ProductCategory.objects.create(**c1)
        cd = {"category":self.productcategory, "quantity_required":2, "percent_discount":"0.20" }
        self.instance = CategoryDiscount.objects.create(**cd)
         
    def test_get_all(self):
        queryset = CategoryDiscount.objects.all()
        super(CategoryDiscountAPITestCase, self).test_get_all("/api/discounts/categories/", queryset)
         
    def test_get_one(self):
        queryset = CategoryDiscount.objects.filter(id = self.instance.id)
        super(CategoryDiscountAPITestCase, self).test_get_one("/api/discounts/categories/1/", queryset)
     
    def test_post(self):
        queryset = CategoryDiscount.objects.filter(id = 2)
        post_data = '{"category":"%s", "quantity_required":3, "percent_discount":"0.50" }' % self.productcategory.uid
        super(CategoryDiscountAPITestCase, self).test_post("/api/discounts/categories/", queryset, post_data)
         
    def test_put(self):
        queryset = CategoryDiscount.objects.filter(id = self.instance.id)
        put_data = '{"category":"%s", "quantity_required":10, "percent_discount":"0.20" }' % self.productcategory.uid
        super(CategoryDiscountAPITestCase, self).test_put("/api/discounts/categories/1/", queryset, put_data)
        self.assertEqual(queryset[0].quantity_required, 10)
         
    def test_delete(self):
        queryset = CategoryDiscount.objects.filter(id = self.instance.id)
        super(CategoryDiscountAPITestCase, self).test_delete("/api/discounts/categories/1/", queryset)

#Test for the loyalty discount API
#See BaseApiTestCase for more details
class LoyaltyDiscountAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        ld = {"revenue_required":"1000.00", "percent_discount":"0.10"}
        self.instance = LoyaltyDiscount.objects.create(**ld)
         
    def test_get_all(self):
        queryset = LoyaltyDiscount.objects.all()
        super(LoyaltyDiscountAPITestCase, self).test_get_all("/api/discounts/loyalty/", queryset)
         
    def test_get_one(self):
        queryset = LoyaltyDiscount.objects.filter(id = 1)
        super(LoyaltyDiscountAPITestCase, self).test_get_one("/api/discounts/loyalty/1/", queryset)
     
    def test_post(self):
        queryset = LoyaltyDiscount.objects.filter(id = 2)
        post_data = '{"revenue_required":"100.00", "percent_discount":"0.10"}'
        super(LoyaltyDiscountAPITestCase, self).test_post("/api/discounts/loyalty/", queryset, post_data)
         
    def test_put(self):
        queryset = LoyaltyDiscount.objects.filter(id = 1)
        put_data = '{"revenue_required":"2000.00", "percent_discount":"0.10"}'
        super(LoyaltyDiscountAPITestCase, self).test_put("/api/discounts/loyalty/1/", queryset, put_data)
        self.assertEqual(queryset[0].revenue_required, 2000)
         
    def test_delete(self):
        queryset = LoyaltyDiscount.objects.filter(id = 1)
        super(LoyaltyDiscountAPITestCase, self).test_delete("/api/discounts/loyalty/1/", queryset)

#Test for the calculate dicount API
class CalculateDiscountsAPITestCase(TestCase):
    json_content_type = "application/json"
    
    #Load the fixtures which contain the initial data we need
    fixtures = [
                'customers/fixtures/initial_data.json',
                'products/fixtures/initial_data.json',
                'discounts/fixtures/initial_data.json'
                ]
    def setUp(self):
        self.client = Client()
        
        #The data to represent an order
        self.data = {
        "id": "2",
        "customer-id": "2",
        "total": "242.3",
        "items": [
            {
              "product-id": "B102",
              "quantity": "5",
              "unit-price": "4.99",
              "total": "24.95"
            },
            {
              "product-id": "B102",
              "quantity": "5",
              "unit-price": "4.99",
              "total": "24.95"
            }, 
            {
              "product-id": "A101",
              "quantity": "2",
              "unit-price": "9.75",
              "total": "19.50"
            },
            {
              "product-id": "A102",
              "quantity": "1",
              "unit-price": "49.50",
              "total": "49.50"
            },
                        {
              "product-id": "B102",
              "quantity": "5",
              "unit-price": "4.99",
              "total": "24.95"
            },
                    {
              "product-id": "B102",
              "quantity": "5",
              "unit-price": "4.99",
              "total": "24.95"
            }, {
              "product-id": "A101",
              "quantity": "2",
              "unit-price": "9.75",
              "total": "19.50"
            },
            {
              "product-id": "A102",
              "quantity": "1",
              "unit-price": "49.50",
              "total": "49.50"
            }
        ]
    } 
    
    def test_get(self):
        #Send the request with the data to the api
        response = self.client.post('/api/discounts/calculate/', json.dumps(self.data), content_type = self.json_content_type)
        
        #Test response attributes
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], self.json_content_type)
        
        #Test the main keys
        data = json.loads(response.content)
        self.assertEqual(data['new_total'], "216.315000")
        self.assertEqual(data['loyalty_discount'], "24.035000")
        
        #Test the items
        self.assertEqual(len(data['items']), 3)
        self.assertEqual(data['items'][0]['free_products']['to_receive'], 4)
        self.assertEqual(data['items'][1]['free_products'], None)
        self.assertEqual(data['items'][2]['free_products'], None)
        
        #Test category discounts
        self.assertEqual(len(data['category_discounts']), 2)
        self.assertEqual(data['category_discounts'][0]["cheapest_product_discount"], 0.0)
        self.assertEqual(data['category_discounts'][0]["cheapest_product_discount_details"], None)
        self.assertEqual(data['category_discounts'][0]["new_total"], 99.8)
        self.assertEqual(data['category_discounts'][1]["cheapest_product_discount"], 1.95)
        self.assertEqual(type(data['category_discounts'][1]["cheapest_product_discount_details"]), type({}))
        self.assertEqual(data['category_discounts'][1]["new_total"], 136.05)
        
        







