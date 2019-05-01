docker-compose -f deployment/docker-compose-peer1.yml up -d
sleep 5
docker-compose -f deployment/docker-compose-cli1.yml up -d
echo "Next step: run depIns4.sh on Instance 4."