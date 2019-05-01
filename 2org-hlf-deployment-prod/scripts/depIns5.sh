docker-compose -f deployment/docker-compose-peer3.yml up -d
sleep 10
docker-compose -f deployment/docker-compose-cli3.yml up -d
echo "Next step: run I2_createChannel.sh on Instance 2."