docker-compose up -d

#For some reason, nginx doesnt start properly after building
#Restarting the containers seems to fix it
echo "Stop containers..."
docker stop djangoApp
docker stop djangoAppDB
docker-compose up -d