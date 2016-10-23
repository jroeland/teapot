from django.contrib import admin
from customers.models import Customer

#Register models to show in the admin interface
admin.site.register(Customer)