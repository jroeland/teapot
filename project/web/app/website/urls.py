from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/customers/', include('customers.urls')),
    url(r'^api/products/', include('products.urls')),
    url(r'^api/discounts/', include('discounts.urls'))
]
