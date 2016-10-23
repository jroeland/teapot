from __future__ import unicode_literals

from django.db import models
from utils.models import Uid
# Create your models here.
class ProductCategory(Uid):
    description = models.CharField(max_length = 64, default = "", blank = False, null = False)
    
    def __unicode__(self):
        return "%s, %s" % (self.uid, self.description)

class Product(Uid):
    description = models.CharField(max_length = 64, default = "", blank = False, null = False)
    category = models.ForeignKey(ProductCategory, to_field = "uid")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __unicode__(self):
        return "%s, %s - %s: %0.2f" % (self.uid, self.description, self.category.description, self.price)