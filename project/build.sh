docker-compose up -d
docker-compose run web python /home/docker/code/app/manage.py migrate
docker-compose run web python /home/docker/code/app/manage.py loaddata /home/docker/code/app/customers/fixtures/initial_data.json
docker-compose run web python /home/docker/code/app/manage.py loaddata /home/docker/code/app/products/fixtures/initial_data.json