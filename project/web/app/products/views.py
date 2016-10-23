from products.models import Product, ProductCategory
from RestApi.TeapotAPI import TeapotAPI
from products.forms import ProductForm, ProductCategoryForm
# Create your views here.
class ProductView(TeapotAPI):
    def __init__(self, *args, **kwargs):
        super(ProductView, self).__init__(*args, **kwargs)
        self.set_model(Product)
        self.set_modelform(ProductForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("uid")
    
class ProductCategoryView(TeapotAPI):
    def __init__(self, *args, **kwargs):
        super(ProductCategoryView, self).__init__(*args, **kwargs)
        self.set_model(ProductCategory)
        self.set_modelform(ProductCategoryForm)
        self.set_allowed_methods(("put", "post", "get", "delete"))
        self.set_lookup_field("uid")