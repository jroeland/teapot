echo "Stop containers..."
docker stop djangoApp
docker stop djangoAppDB
docker-compose up -d