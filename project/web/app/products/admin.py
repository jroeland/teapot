from django.contrib import admin
from products.models import Product, ProductCategory

#Register models to show in the admin interface
admin.site.register(Product)
admin.site.register(ProductCategory)