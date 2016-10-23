# Teapot

Teapot is a python-django based application wrapped in
docke-compose which calculates discounts for orders.

## Features
- A simple REST-API which can be easely used in class based views
- Unit-tests
- Admin interface

## Install instructions - Fast (Tested only in linux-debian based distributions)
Requirements:
- pip

It is possible to runproject without having to use docker-compose.
Simply edit the following file:

    /project/web/app/website/settings.py

Change the following variable to True:

    TEST = False
    
Run the following file, which will install the requirements using pip, run
the migrations and load the initial data.
Note: Its recommended to run this command in a virttual env, although
it will still work if ran globally:

    cd project/
    . /easy_build.sh

Now start the django's development server with the following command:

    cd project/web/app/
    python manage.py runserver localhost:8080
    
To run the tests, run the following command:

    cd project/web/app/
    python manage.py runserver localhost:8080

## Install instructions - docker-compose
To build the project as a micro-service, run the following command:

    cd project/
    . build.sh

If you have made some changes to the docker file and you wish to re-build the service:

    cd project/
    . rebuildAll.sh

### Some extra management commands when using the service:
To stop the service:

    cd project/
    . stop.sh

To start / restart the service:

    cd project/
    . start.sh

To run the tests:

    cd project/
    . runTests.sh

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

## Admin Interface
To facitilate operations, the admin site is available.
To login to the admin interface, go to /admin/
- Username: admin
- Password: teapotapi

