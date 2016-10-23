from __future__ import unicode_literals

from django.db import models

#Some of the data to use in the given examples have an id
#In order for not to interfere with django's id system, we will use this field instead
class Uid(models.Model):
    class Meta:
        abstract = True
    uid = models.CharField(max_length = 4, db_index = True, unique = True, default = "", blank = False, null = False)