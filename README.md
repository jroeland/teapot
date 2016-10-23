# Teapot

Teapot is a python-django based application wrapped in
docke-compose which calculates discounts for orders.

## Features
- A simple REST-API which can be easely used in class based views
- Unit-tests
- Anti-cheat system

## End-points

The end-points for customers:
    /api/customers/ accepts GET, POST requests
    /api/customers/\<id\>/ accepts GET, PUT and DELETE requests

The end-points for products:
    /api/products/ accepts GET, POST requests
    /api/products/\<id\>/ accepts GET, PUT and DELETE requests

The end-points for product categories:
    /api/products/categories/ accepts GET, POST requests
    /api/products/categories/\<id\>/ accepts GET, PUT and DELETE requests
    
The end-points for free product discounts:
    /api/discounts/freeproducts/ accepts GET, POST requests
    /api/discounts/freeproducts/\<id\>/ accepts GET, PUT and DELETE requests

The end-points for category discounts:
    /api/discounts/categories/ accepts GET, POST requests
    /api/discounts/categories/\<id\>/ accepts GET, PUT and DELETE requests

The end-points for cutomer loyalty discounts:
    /api/discounts/loyalty/ accepts GET, POST requests
    /api/discounts/loyalty/\<id\>/ accepts GET, PUT and DELETE requests
    
The end-points to calculate discounts for an order:
    /api/discounts/calculate/ accepts POST requests
