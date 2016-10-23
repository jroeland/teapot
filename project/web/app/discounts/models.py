from __future__ import unicode_literals
from django.db import models
from products.models import ProductCategory, Product


class FreeProduct(models.Model):
    product = models.ForeignKey(Product, to_field = "uid")
    quantity_required = models.IntegerField(default = 1)
    
    
    class Meta:
        #Accept only 1 unique combination of products and quantity
        unique_together = ('product', 'quantity_required',)
    
    def __unicode__(self):
        return "%s, Quantity: %d" % (self.product.description, self.quantity_required)
    
class CategoryDiscount(models.Model):
    category = models.ForeignKey(ProductCategory, to_field = "uid")
    quantity_required = models.IntegerField(default = 1)
    percent_discount = models.DecimalField(max_digits=3, decimal_places=2, default = 0, help_text = "Percent dicount to apply to the cheapest product")
    
    def __unicode__(self):
        return "%s, Quantity: %d, discount: %0.2f" % (self.category.description, self.quantity_required, self.percent_discount)
    
class LoyaltyDiscount(models.Model):
    revenue_required = models.DecimalField(default = 0, max_digits=10, decimal_places=2, blank = False, null = False)
    percent_discount = models.DecimalField(max_digits=3, decimal_places=2, default = 0, help_text = "Percent dicount to apply to the cheapest product")
    
    def __unicode__(self):
        return "revenue required: %0.2f, discount: %0.2f" % (self.revenue_required, self.percent_discount)