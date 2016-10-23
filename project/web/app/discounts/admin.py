from django.contrib import admin
from discounts.models import FreeProduct, CategoryDiscount, LoyaltyDiscount

#Register models to show in the admin interface
admin.site.register(FreeProduct)
admin.site.register(CategoryDiscount)
admin.site.register(LoyaltyDiscount)