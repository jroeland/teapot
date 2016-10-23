# Run the migrations
python /home/docker/code/app/manage.py migrate

#Add the initial fixtures
python /home/docker/code/app/manage.py loaddata /home/docker/code/app/admin/fixtures/initial_data.json
python /home/docker/code/app/manage.py loaddata /home/docker/code/app/customers/fixtures/initial_data.json
python /home/docker/code/app/manage.py loaddata /home/docker/code/app/products/fixtures/initial_data.json
python /home/docker/code/app/manage.py loaddata /home/docker/code/app/discounts/fixtures/initial_data.json

#Start the server
supervisord -n