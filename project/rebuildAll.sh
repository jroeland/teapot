docker stop djangoApp
docker stop djangoAppDB
docker rm djangoApp djangoAppDB --force
docker rmi epicproject_web postgres --force
docker-compose up -d