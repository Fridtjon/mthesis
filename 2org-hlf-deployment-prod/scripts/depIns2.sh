docker-compose -f deployment/docker-compose-peer0.yml up -d
sleep 5
docker-compose -f deployment/docker-compose-cli0.yml up -d
echo "Next step: run depIns3.sh on Instance 3."