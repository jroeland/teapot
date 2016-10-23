from django.test import TestCase, Client
from products.models import Product, ProductCategory
from RestApi.testbase import BaseApiTestCase

#Test for the product API
#See BaseApiTestCase for more details
class ProductAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        c1 = {"description":"Tools", "uid" : "1"}
        pc = ProductCategory.objects.create(**c1)
        p1 = {"uid":"A101", "description":"Screwdriver", "category":pc, "price":"9.75"}
        Product.objects.create(**p1)
        
    def test_get_all(self):
        queryset = Product.objects.all()
        super(ProductAPITestCase, self).test_get_all("/api/products/", queryset)
        
    def test_get_one(self):
        queryset = Product.objects.filter(uid = "A101")
        super(ProductAPITestCase, self).test_get_one("/api/products/A101/", queryset)
    
    def test_post(self):
        queryset = Product.objects.filter(uid = "A102")
        post_data = '{"uid":"A102", "description":"Electric screwdriver", "category":"1", "price":"49.50"}'
        super(ProductAPITestCase, self).test_post("/api/products/", queryset, post_data)
        
    def test_put(self):
        queryset = Product.objects.filter(uid = "A101")
        put_data = '{"uid":"A101", "description":"Screwdriverrrrr", "category":"1", "price":"9.75"}'
        super(ProductAPITestCase, self).test_put("/api/products/A101/", queryset, put_data)
        self.assertEqual(queryset[0].description, "Screwdriverrrrr")
        
    def test_delete(self):
        queryset = Product.objects.filter(uid = "A101")
        super(ProductAPITestCase, self).test_delete("/api/products/A101/", queryset)
        
#Test for the product category API
#See BaseApiTestCase for more details
class ProductCategoryAPITestCase(BaseApiTestCase, TestCase):
    def setUp(self):
        self.client = Client()
        c1 = {"description":"Tools", "uid" : "1"}
        ProductCategory.objects.create(**c1)
        
    def test_get_all(self):
        queryset = ProductCategory.objects.all()
        super(ProductCategoryAPITestCase, self).test_get_all("/api/products/categories/", queryset)
        
    def test_get_one(self):
        queryset = ProductCategory.objects.filter(uid = "1")
        super(ProductCategoryAPITestCase, self).test_get_one("/api/products/categories/1/", queryset)
    
    def test_post(self):
        queryset = ProductCategory.objects.filter(uid = "2")
        post_data = '{"description":"Switches", "uid" : "2"}'
        super(ProductCategoryAPITestCase, self).test_post("/api/products/categories/", queryset, post_data)
        
    def test_put(self):
        queryset = ProductCategory.objects.filter(uid = "1")
        put_data = '{"description":"Toolssss", "uid" : "1"}'
        super(ProductCategoryAPITestCase, self).test_put("/api/products/categories/1/", queryset, put_data)
        self.assertEqual(queryset[0].description, "Toolssss")
        
    def test_delete(self):
        queryset = ProductCategory.objects.filter(uid = "1")
        super(ProductCategoryAPITestCase, self).test_delete("/api/products/categories/1/", queryset)