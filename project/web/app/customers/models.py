from __future__ import unicode_literals

from django.db import models
from datetime import date
from utils.models import Uid

#The customer model
class Customer(Uid):
    name = models.CharField(max_length = 16, default = "", blank = False, null = False)
    since = models.DateField(default = date.today, blank = False, null = False)
    revenue = models.DecimalField(default = 0, max_digits=10, decimal_places=2, blank = False, null = False)
    def __unicode__(self):
        return "%d - Uid: %s, %s - %s, %0.2f" % (self.id, self.uid, self.name, self.since, self.revenue)