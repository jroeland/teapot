#Use easy build when TEST = True in the settings file.
#Then we can use the default django db (sqlite) and run
#the project using django's built-in server

#Install dependencies
pip install -r web/app/requirements.txt
python web/app/manage.py migrate
python web/app/manage.py loaddata web/app/admin/fixtures/initial_data.json
python web/app/manage.py loaddata web/app/customers/fixtures/initial_data.json
python web/app/manage.py loaddata web/app/products/fixtures/initial_data.json
python web/app/manage.py loaddata web/app/discounts/fixtures/initial_data.json
python web/app/manage.py collectstatic <<<yes