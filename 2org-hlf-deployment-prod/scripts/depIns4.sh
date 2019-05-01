docker-compose -f deployment/docker-compose-peer2.yml up -d
sleep 10
docker-compose -f deployment/docker-compose-cli2.yml up -d
echo "Next step: run depIns5.sh on Instance 5."